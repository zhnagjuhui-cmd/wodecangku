"""Offline behavioral tests; no generation tools or network calls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

SCRIPT = Path(__file__).with_name('image_jobs.py')


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.queue = self.root/'run'
        self.source = self.root/'source.png'
        Image.new('RGB',(80,40),'red').save(self.source)

    def tearDown(self):
        self.temp.cleanup()

    def cmd(self,name,*args,code=0):
        p = subprocess.run([sys.executable,str(SCRIPT),name,'--queue',str(self.queue),*map(str,args)],
                           capture_output=True,text=True)
        self.assertEqual(p.returncode,code,p.stdout+p.stderr)
        try:
            return json.loads(p.stdout or p.stderr)
        except json.JSONDecodeError:
            return {'message':p.stdout or p.stderr}

    def init(self,jobs):
        path = self.root/'jobs.jsonl'
        path.write_text('\n'.join(json.dumps(j) for j in jobs),encoding='utf-8')
        return self.cmd('init','--jobs',path)

    def recorded(self,size='80x40',**extra):
        self.init([{'id':'a','prompt':'test','size':size,**extra}])
        self.cmd('claim')
        self.cmd('record','--id','a','--image',self.source)

    def test_mismatch_requires_explicit_acceptance(self):
        self.recorded('100x100')
        job = self.cmd('finish','--id','a')
        self.assertFalse(job['validation']['size_matches'])
        self.assertEqual(Path(job['output']).read_bytes(),self.source.read_bytes())
        self.cmd('approve','--id','a',code=2)
        self.assertEqual(self.cmd('approve','--id','a','--accept-actual-size')['status'],'completed')

    def test_contain_preserves_original_and_versions_output(self):
        self.recorded('100x100')
        first = self.cmd('finish','--id','a')
        before = Path(first['output']).read_bytes()
        fitted = self.cmd('finish','--id','a','--fit','contain')
        self.assertNotEqual(first['output'],fitted['output'])
        self.assertEqual(Path(first['output']).read_bytes(),before)
        self.assertEqual(Path(fitted['original']).read_bytes(),self.source.read_bytes())
        with Image.open(fitted['output']) as im:
            self.assertEqual(im.size,(100,100))
            self.assertEqual(im.getpixel((0,0)),(255,255,255,255))
            self.assertEqual(im.getpixel((50,50)),(255,0,0,255))
        self.assertTrue(fitted['validation']['upscaled'])
        self.cmd('approve','--id','a')

    def test_alpha_preserved_and_missing_alpha_rejected(self):
        Image.new('RGBA',(80,40),(0,0,255,100)).save(self.source)
        self.recorded('100x100',transparent_background=True)
        job = self.cmd('finish','--id','a','--fit','contain')
        self.assertTrue(job['validation']['transparency_ok'])
        self.cmd('approve','--id','a')

    def test_opaque_result_cannot_pass_transparent_job(self):
        self.recorded(transparent_background=True)
        self.cmd('finish','--id','a')
        self.cmd('approve','--id','a',code=2)

    def test_edit_reference_resolution_and_alpha_default(self):
        Image.new('RGBA',(10,10),(1,2,3,0)).save(self.source)
        self.init([{'id':'a','prompt':'watercolor','operation':'style-transfer',
                    'references':[{'path':'source.png','role':'target'}]}])
        job = self.cmd('claim')
        self.assertEqual(job['references'][0]['path'],str(self.source.resolve()))
        self.assertTrue(job['transparent_background'])

    def test_invalid_batch_does_not_create_queue(self):
        self.init_bad([{'id':'a','prompt':'edit','operation':'edit'}])
        self.init_bad([{'id':'a','prompt':'x'},{'id':'a','prompt':'y'}])

    def init_bad(self,jobs):
        path = self.root/'invalid.jsonl'
        path.write_text('\n'.join(json.dumps(j) for j in jobs))
        self.cmd('init','--jobs',path,code=2)
        self.assertFalse(self.queue.exists())

    def test_concurrent_claim_cannot_duplicate(self):
        self.init([{'id':'a','prompt':'one'},{'id':'b','prompt':'two'}])
        argv = [sys.executable,str(SCRIPT),'claim','--queue',str(self.queue)]
        p1 = subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        p2 = subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        p1.communicate(timeout=10)
        p2.communicate(timeout=10)
        self.assertEqual(sorted([p1.returncode,p2.returncode]),[0,2])
        self.assertEqual(self.cmd('status')['counts'],{'running':1,'pending':1})

    def test_recovery_does_not_regenerate(self):
        self.recorded()
        job = self.cmd('finish','--id','a')
        self.assertEqual(job['attempts'],1)
        self.cmd('approve','--id','a')
        self.cmd('poll','--timeout','0')

    def test_retry_keeps_history_and_requires_ack(self):
        self.init([{'id':'a','prompt':'x'}])
        self.cmd('claim')
        self.cmd('retry','--id','a',code=2)
        self.cmd('fail','--id','a','--reason','uncertain')
        self.cmd('retry','--id','a','--ack-duplicate-risk')
        job = self.cmd('claim')
        self.assertEqual(job['attempts'],2)
        self.assertEqual([x['status'] for x in job['history']],['running','failed','pending','running'])

    def test_changed_output_cannot_be_approved(self):
        self.recorded()
        job = self.cmd('finish','--id','a')
        Image.new('RGB',(80,40),'blue').save(job['output'])
        self.cmd('approve','--id','a',code=2)

    def test_batch_flow_and_poll_exit_codes(self):
        self.init([{'id':'a','prompt':'one'},{'id':'b','prompt':'two'}])
        self.cmd('poll','--timeout','0',code=3)
        self.cmd('claim')
        self.cmd('claim',code=2)
        self.cmd('record','--id','a','--image',self.source)
        self.cmd('finish','--id','a')
        self.cmd('approve','--id','a')
        self.assertEqual(self.cmd('claim')['id'],'b')
        self.cmd('cancel','--id','b','--reason','user cancelled')
        self.cmd('poll','--timeout','0',code=2)

    def test_jpeg_kept_as_jpeg(self):
        path = self.root/'photo.jpg'
        Image.new('RGB',(80,40),'red').save(path)
        self.recorded()
        # Restore fixture state to record the JPEG, without generating anything.
        self.cmd('retry','--id','a','--ack-duplicate-risk')
        self.cmd('claim')
        self.cmd('record','--id','a','--image',path)
        job = self.cmd('finish','--id','a')
        self.assertEqual(Path(job['output']).suffix,'.jpg')
        self.assertEqual(Path(job['output']).read_bytes(),path.read_bytes())


if __name__=='__main__':
    unittest.main()
