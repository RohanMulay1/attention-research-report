"""Numbers for the report, generated from the source repositories.

DO NOT EDIT. Regenerate with `python sync_values.py`.

Every entry records the file it came from and the row that selected
it, so a number in the PDF can be traced to a committed measurement
without trusting this file.
"""

GENERATED = '2026-09-06T06:14:18Z'
SOURCES = {
    'xsa_controls': '0f312c061fd707e237691c65789f719d84bc0ddb',
    'crpa': '31b9e30436f72e22e4459b72867b1f1a262d4549',
}

VALUES = {
    'a2.gpt2.cos_self.ceiling': {'value': 0.8903322196538361, 'text': '0.890', 'source': 'results/a2_correlations.csv', 'selector': 'model=gpt2,statistic=cos_self'},
    'a2.gpt2.cos_self.disatt': {'value': 0.5190029420422932, 'text': '+0.519', 'source': 'results/a2_correlations.csv', 'selector': 'model=gpt2,statistic=cos_self'},
    'a2.gpt2.cos_self.rho': {'value': 0.46208504139538625, 'text': '+0.462', 'source': 'results/a2_correlations.csv', 'selector': 'model=gpt2,statistic=cos_self'},
    'a2.gpt2.excess.ceiling': {'value': 0.890511720671711, 'text': '0.891', 'source': 'results/a2_correlations.csv', 'selector': 'model=gpt2,statistic=excess'},
    'a2.gpt2.excess.disatt': {'value': 0.31283463751762586, 'text': '+0.313', 'source': 'results/a2_correlations.csv', 'selector': 'model=gpt2,statistic=excess'},
    'a2.gpt2.excess.rho': {'value': 0.278582911341532, 'text': '+0.279', 'source': 'results/a2_correlations.csv', 'selector': 'model=gpt2,statistic=excess'},
    'a2.gpt2.r_delta': {'value': 0.7953862229724299, 'text': '+0.795', 'source': 'results/reliability.csv', 'selector': 'model=gpt2'},
    'a2.gpt2.seq_len': {'value': 128.0, 'text': '128', 'source': 'results/reliability.csv', 'selector': 'model=gpt2'},
    'a2.gpt2.verdict': {'value': 'reliable', 'text': 'reliable', 'source': 'results/reliability.csv', 'selector': 'model=gpt2'},
    'a2.pythia-160m.cos_self.ceiling': {'value': 0.6451639414346071, 'text': '0.645', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-160m,statistic=cos_self'},
    'a2.pythia-160m.cos_self.disatt': {'value': 0.23107251723447134, 'text': '+0.231', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-160m,statistic=cos_self'},
    'a2.pythia-160m.cos_self.rho': {'value': 0.1490796559762077, 'text': '+0.149', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-160m,statistic=cos_self'},
    'a2.pythia-160m.excess.ceiling': {'value': 0.6455290095351548, 'text': '0.646', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-160m,statistic=excess'},
    'a2.pythia-160m.excess.disatt': {'value': 0.29227272839881047, 'text': '+0.292', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-160m,statistic=excess'},
    'a2.pythia-160m.excess.rho': {'value': 0.18867052487742142, 'text': '+0.189', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-160m,statistic=excess'},
    'a2.pythia-160m.r_delta': {'value': 0.41872036009967045, 'text': '+0.419', 'source': 'results/reliability.csv', 'selector': 'model=EleutherAI/pythia-160m'},
    'a2.pythia-160m.seq_len': {'value': 128.0, 'text': '128', 'source': 'results/reliability.csv', 'selector': 'model=EleutherAI/pythia-160m'},
    'a2.pythia-160m.verdict': {'value': 'attenuated', 'text': 'attenuated', 'source': 'results/reliability.csv', 'selector': 'model=EleutherAI/pythia-160m'},
    'a2.pythia-410m.cos_self.ceiling': {'value': 0.7255451058258096, 'text': '0.726', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-410m,statistic=cos_self'},
    'a2.pythia-410m.cos_self.disatt': {'value': -0.03384242870572599, 'text': '-0.034', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-410m,statistic=cos_self'},
    'a2.pythia-410m.cos_self.rho': {'value': -0.02455420851669838, 'text': '-0.025', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-410m,statistic=cos_self'},
    'a2.pythia-410m.excess.ceiling': {'value': 0.7268651936662681, 'text': '0.727', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-410m,statistic=excess'},
    'a2.pythia-410m.excess.disatt': {'value': 0.3423134795094323, 'text': '+0.342', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-410m,statistic=excess'},
    'a2.pythia-410m.excess.rho': {'value': 0.2488157535781976, 'text': '+0.249', 'source': 'results/a2_correlations.csv', 'selector': 'model=EleutherAI/pythia-410m,statistic=excess'},
    'a2.pythia-410m.r_delta': {'value': 0.5309859363873725, 'text': '+0.531', 'source': 'results/reliability.csv', 'selector': 'model=EleutherAI/pythia-410m'},
    'a2.pythia-410m.seq_len': {'value': 128.0, 'text': '128', 'source': 'results/reliability.csv', 'selector': 'model=EleutherAI/pythia-410m'},
    'a2.pythia-410m.verdict': {'value': 'attenuated', 'text': 'attenuated', 'source': 'results/reliability.csv', 'selector': 'model=EleutherAI/pythia-410m'},
    'crpa.ctx16384.delta_max': {'value': 1.9073486328125e-06, 'text': '1.91e-06', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=16384'},
    'crpa.ctx16384.overlap': {'value': 0.2297086107863015, 'text': '0.2297', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=16384'},
    'crpa.ctx16384.peak_gb': {'value': 1.2441673278808594, 'text': '1.24', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=16384'},
    'crpa.ctx32768.delta_max': {'value': 9.5367431640625e-07, 'text': '9.54e-07', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=32768'},
    'crpa.ctx32768.overlap': {'value': 0.23084974854006704, 'text': '0.2308', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=32768'},
    'crpa.ctx32768.peak_gb': {'value': 1.9277076721191406, 'text': '1.93', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=32768'},
    'crpa.ctx4096.delta_max': {'value': 9.5367431640625e-07, 'text': '9.54e-07', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=4096'},
    'crpa.ctx4096.overlap': {'value': 0.22653466018915838, 'text': '0.2265', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=4096'},
    'crpa.ctx4096.peak_gb': {'value': 0.7516093254089355, 'text': '0.75', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=4096'},
    'crpa.ctx65536.delta_max': {'value': 9.5367431640625e-07, 'text': '9.54e-07', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=65536'},
    'crpa.ctx65536.overlap': {'value': 0.23028840694268898, 'text': '0.2303', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=65536'},
    'crpa.ctx65536.peak_gb': {'value': 3.302906036376953, 'text': '3.30', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=65536'},
    'crpa.ctx8192.delta_max': {'value': 9.5367431640625e-07, 'text': '9.54e-07', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=8192'},
    'crpa.ctx8192.overlap': {'value': 0.22561001350613485, 'text': '0.2256', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=8192'},
    'crpa.ctx8192.peak_gb': {'value': 1.1517419815063477, 'text': '1.15', 'source': 'results/tier2_bounded_v2/long_context.csv', 'selector': 'context_length=8192'},
    'gqa.Qwen2.5-0.5B.across': {'value': -0.1876071131905386, 'text': '-0.1876', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-0.5B'},
    'gqa.Qwen2.5-0.5B.kv_heads': {'value': 2.0, 'text': '2', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-0.5B'},
    'gqa.Qwen2.5-0.5B.q_heads': {'value': 14.0, 'text': '14', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-0.5B'},
    'gqa.Qwen2.5-0.5B.within': {'value': 0.2415065986403405, 'text': '+0.2415', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-0.5B'},
    'gqa.Qwen2.5-1.5B.across': {'value': -0.1922146026692474, 'text': '-0.1922', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-1.5B'},
    'gqa.Qwen2.5-1.5B.kv_heads': {'value': 2.0, 'text': '2', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-1.5B'},
    'gqa.Qwen2.5-1.5B.q_heads': {'value': 12.0, 'text': '12', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-1.5B'},
    'gqa.Qwen2.5-1.5B.within': {'value': 0.2731452193544608, 'text': '+0.2731', 'source': 'results/gqa.csv', 'selector': 'model=Qwen/Qwen2.5-1.5B'},
    'gqa.TinyLlama-1.1B.across': {'value': -0.1126472965588957, 'text': '-0.1126', 'source': 'results/gqa.csv', 'selector': 'model=TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T'},
    'gqa.TinyLlama-1.1B.kv_heads': {'value': 4.0, 'text': '4', 'source': 'results/gqa.csv', 'selector': 'model=TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T'},
    'gqa.TinyLlama-1.1B.q_heads': {'value': 32.0, 'text': '32', 'source': 'results/gqa.csv', 'selector': 'model=TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T'},
    'gqa.TinyLlama-1.1B.within': {'value': 0.23733443375483418, 'text': '+0.2373', 'source': 'results/gqa.csv', 'selector': 'model=TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T'},
    'paired.primary.random.ci_high': {'value': 0.0023903968881388016, 'text': '+0.002390', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.random.ci_low': {'value': -0.00029788990734047616, 'text': '-0.000298', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.random.mde': {'value': 0.0021484076372337707, 'text': '0.00215', 'source': 'results/paired_tests_s.csv', 'selector': '2.9 * sd_paired / sqrt(n_seeds), arm=random'},
    'paired.primary.random.mean_delta': {'value': 0.0010564744350363142, 'text': '+0.001056', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.random.n_seeds': {'value': 8.0, 'text': '8', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.random.p': {'value': 0.1968845256913458, 'text': '0.197', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.random.sd_paired': {'value': 0.0020953842883323693, 'text': '0.002095', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.random.t': {'value': 1.4260682230445534, 'text': '+1.43', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=random'},
    'paired.primary.xsa.ci_high': {'value': -0.0017092869189552413, 'text': '-0.001709', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'paired.primary.xsa.ci_low': {'value': -0.003966764104170795, 'text': '-0.003967', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'paired.primary.xsa.mde': {'value': 0.0018174300817321105, 'text': '0.00182', 'source': 'results/paired_tests_s.csv', 'selector': '2.9 * sd_paired / sqrt(n_seeds), arm=xsa'},
    'paired.primary.xsa.mean_delta': {'value': -0.002923833420042099, 'text': '-0.002924', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'paired.primary.xsa.n_seeds': {'value': 8.0, 'text': '8', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'paired.primary.xsa.p': {'value': 0.002299759318182331, 'text': '0.002', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'paired.primary.xsa.sd_paired': {'value': 0.001772575358793375, 'text': '0.001773', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'paired.primary.xsa.t': {'value': -4.665443256029428, 'text': '-4.67', 'source': 'results/paired_tests_s.csv', 'selector': 'arm=xsa'},
    'planning.mde': {'value': 0.005176429127486357, 'text': '0.00518', 'source': 'results/pilot_decision.json', 'selector': 'Day-3 planning forecast'},
    'planning.sigma_paired': {'value': 0.005048673294313334, 'text': '0.00505', 'source': 'results/pilot_decision.json', 'selector': 'Day-3 planning forecast'},
}


def V(key):
    """Rendered text for one value, or a loud marker if absent."""
    entry = VALUES.get(key)
    if entry is None:
        raise KeyError(
            'no generated value for %r; run sync_values.py' % key)
    return entry['text']


def num(key):
    """The raw value, for arithmetic in the content module."""
    return VALUES[key]['value']
