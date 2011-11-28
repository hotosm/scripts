import os
import sys
import unittest

test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(test_dir,'../'))

import preset2style

class TestPreset(unittest.TestCase):

    def test_open(self):
        style = preset2style.Osm2PgsqlStyle()
        self.assertEqual(style.rules, {})

    def test_error_on_space(self):
        style = preset2style.Osm2PgsqlStyle()
        preset = os.path.join(test_dir,'preset_with_invalid_keys.xml')
        self.assertRaises(ValueError,style.merge_josm_preset_keys, preset)

    def test_error_on_empty_preset(self):
        style = preset2style.Osm2PgsqlStyle()
        preset = os.path.join(test_dir,'empty_preset.xml')
        self.assertRaises(RuntimeError,style.merge_josm_preset_keys, preset)

    def test_preset_with_ns(self):
        style = preset2style.Osm2PgsqlStyle()
        preset = os.path.join(test_dir,'preset_with_ns.xml')
        style.merge_josm_preset_keys(preset)
        self.assertEqual(len(style.rules), 1)
        tag = style.rules.get('key')
        self.assertEqual(tag['data_type'], 'text')
        self.assertEqual(tag['source'], 'JOSM preset')
        self.assertEqual(tag['in_preset'], True)

    def test_preset_without_ns(self):
        style = preset2style.Osm2PgsqlStyle()
        preset = os.path.join(test_dir,'preset_with_ns.xml')
        style.merge_josm_preset_keys(preset)
        self.assertEqual(len(style.rules), 1)
        tag = style.rules.get('key')
        self.assertEqual(tag['data_type'], 'text')
        self.assertEqual(tag['source'], 'JOSM preset')
        self.assertEqual(tag['in_preset'], True)

    def test_haiti_preset(self):
        style = preset2style.Osm2PgsqlStyle()
        preset = os.path.join(test_dir,'COSMHA_DRR_josm_presets_haiti_v1.05.xml')
        style.merge_josm_preset_keys(preset)
        self.assertEqual(len(style.rules), 203)

class TestDefaultStyle(unittest.TestCase):

    def test_opening_default_style(self):
        style = preset2style.Osm2PgsqlStyle()
        dfl_sty = os.path.join(test_dir,'default.style')
        style.parse_style(dfl_sty)
        self.assertEqual(len(style.rules), 71)

    def test_opening_one_line_style(self):
        style = preset2style.Osm2PgsqlStyle()
        dfl_sty = os.path.join(test_dir,'one_line.style')
        style.parse_style(dfl_sty)
        self.assertEqual(len(style.rules), 1)
        tag = style.rules.get('addr:housename')
        self.assertEqual(tag['data_type'], 'text')
        self.assertEqual(tag['source'], 'osm2pgsql style')
        self.assertEqual(tag['flags'], 'linear')
        self.assertEqual(tag['in_style'], True)
        self.assertEqual(tag['osm_type'], 'node,way')


if __name__ == '__main__':
    unittest.main()