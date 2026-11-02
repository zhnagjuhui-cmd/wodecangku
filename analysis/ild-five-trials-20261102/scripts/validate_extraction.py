#!/usr/bin/env python3
"""Validate structural provenance and missingness; never certify medical truth."""
import copy
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'study_extraction.json'
EXPECTED = {'SENSCIS', 'INBUILD', 'TRAIL1', 'RELIEF', 'U-ILD'}
METRICS = {'sample_size', 'primary_effect', 'primary_ci_lower', 'primary_ci_upper',
           'primary_p_value', 'treatment_fvc_change', 'control_fvc_change',
           'treatment_adverse_events', 'control_adverse_events'}
HIERARCHY = {'PRIMARY', 'KEY_SECONDARY', 'SECONDARY', 'EXPLORATORY', 'SAFETY'}


def validate(data):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    check(data.get('schema_version') == '0.1.0', 'schema version')
    check(bool(data.get('dataset_version')), 'dataset version')
    check(data.get('release_status') == 'DRAFT_NOT_FOR_PRESENTATION', 'release gate')
    studies = data.get('studies', [])
    check(len(studies) == 5 and {s.get('study_id') for s in studies} == EXPECTED,
          'exactly five unique studies required')
    for study in studies:
        sid = study.get('study_id')
        for key in ('record_version', 'extracted_by', 'extracted_at'):
            check(bool(study.get(key)), f'{sid}: {key}')
        check(study.get('verification_status') in {'UNVERIFIED', 'VERIFIED'}, f'{sid}: status')
        check(study.get('review_status') in {'PENDING_INDEPENDENT_REVIEW', 'APPROVED'}, f'{sid}: review')
        if study.get('review_status') == 'APPROVED':
            check(bool(study.get('reviewer')) and bool(study.get('reviewed_at')), f'{sid}: reviewer required')
        source_ids = set()
        for source in study.get('sources', []):
            for key in ('source_id', 'source_type', 'url', 'doi', 'pmid', 'nct',
                        'accessed_at', 'source_version', 'access_level', 'file_sha256'):
                check(key in source, f'{sid}: source missing {key}')
            source_id = source.get('source_id')
            check(bool(source_id) and source_id not in source_ids, f'{sid}: duplicate/empty source id')
            source_ids.add(source_id)
            check(source.get('source_type') in {'ORIGINAL_ARTICLE', 'SUPPLEMENT', 'REGISTRY'}, f'{sid}: source type')
            check(source.get('access_level') in {'FULL_TEXT', 'ABSTRACT_ONLY', 'METADATA_ONLY'}, f'{sid}: access level')
            check(str(source.get('url', '')).startswith('https://'), f'{sid}: source URL')
        metrics = study.get('metrics', [])
        check(len(metrics) == len(METRICS) and {m.get('metric_id') for m in metrics} == METRICS,
              f'{sid}: metrics inventory')
        for metric in metrics:
            label = f'{sid}/{metric.get("metric_id")}'
            for key in ('value', 'unit', 'analysis_population', 'endpoint_hierarchy', 'timepoint',
                        'effect_measure', 'missing_reason', 'verification_status', 'source_id',
                        'source_location', 'source_version', 'review_status'):
                check(key in metric, f'{label}: missing {key}')
            value = metric.get('value')
            check(metric.get('verification_status') in {'UNVERIFIED', 'VERIFIED'}, f'{label}: status')
            check(metric.get('review_status') in {'PENDING_INDEPENDENT_REVIEW', 'APPROVED'}, f'{label}: review')
            if value is None:
                check(bool(metric.get('missing_reason')), f'{label}: missing reason required')
                check(metric.get('verification_status') == 'UNVERIFIED', f'{label}: null cannot be verified')
            else:
                check(isinstance(value, (int, float)) and not isinstance(value, bool), f'{label}: numeric value required')
                check(metric.get('missing_reason') is None, f'{label}: missing must not be filled with number')
                for key in ('unit', 'analysis_population', 'timepoint', 'effect_measure', 'source_location', 'source_version'):
                    check(bool(metric.get(key)), f'{label}: {key} required')
                check(metric.get('endpoint_hierarchy') in HIERARCHY, f'{label}: hierarchy')
                check(metric.get('source_id') in source_ids, f'{label}: unresolved source')
    return errors


if __name__ == '__main__':
    data = json.loads(DATA.read_text(encoding='utf-8'))
    errors = validate(data)
    if errors:
        raise SystemExit('\n'.join(errors))
    missing_reason_removed = copy.deepcopy(data)
    missing_reason_removed['studies'][0]['metrics'][0]['missing_reason'] = None
    assert validate(missing_reason_removed), 'negative control failed: absent missing reason'
    zero_filled = copy.deepcopy(data)
    zero_filled['studies'][0]['metrics'][0]['value'] = 0
    assert validate(zero_filled), 'negative control failed: missing filled with zero'
    print('PASS: 5 studies; 45 null/UNVERIFIED metric slots; provenance structure valid.')
    print('PASS: negative controls reject absent missing reason and zero-filled missing value.')
    print('Medical data verification: NOT PERFORMED; independent acceptance: PENDING.')
