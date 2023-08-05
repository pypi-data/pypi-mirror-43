# coding=utf-8
from __future__ import unicode_literals

import glob
import logging
import os
import yaml
import editdistance

SEPARATOR_CHARS = " -_.:"


class PlateYaml(object):
    def __init__(self, filename):
        self.scheme = ""
        self.version = -1
        self.exactitude = 0.0
        self.filename = filename
        with open(filename, 'r') as f:
            try:
                self.settings = yaml.load(f)
                self.valid_chars = self.settings["allowed"]
                self.exactitude = self.settings["exactitude"]
                self.kept_separators = self.settings.get("kept_separators", "NONE").upper()
                self.replacements = []
                for r in self.settings.get("replacements", []):
                    if r.get("from", "") != "" and "to" in r:
                        self.replacements.append((unicode(r.get("from")), unicode(r.get("to"))))
            except:
                logging.error("Error loading Plate Yaml %s, will be ignored", filename)
                return

        try:
            self.scheme, tmp = os.path.basename(filename).replace(".", "-").split("-")[:2]
            self.version = int(tmp)
        except Exception as e:
            logging.exception(e)
            logging.error("Invalid Plate Yaml filename %s, will be ignored", filename)
            return

    def convert(self, plate):
        plate.upper()
        for r in self.replacements:
            plate = plate.replace(r[0], r[1])
        tmp = plate
        for c in tmp:
            if c not in self.valid_chars:
                plate = plate.replace(c, "")

        if self.kept_separators != "ALL":
            plate_stripped = plate
            for c in list(SEPARATOR_CHARS):
                plate_stripped = plate_stripped.replace(c, "")
            if self.kept_separators == "FIRST":
                for i, c in enumerate(list(plate)):
                    if c in SEPARATOR_CHARS:
                        plate = plate[:i + 1] + plate_stripped[i:]
                        break
            elif self.kept_separators == "LAST":
                for i, c in enumerate(reversed(list(plate))):
                    if c in SEPARATOR_CHARS:
                        plate = plate_stripped[:-i] + plate[-1 - i:]
                        break
            else:
                plate = plate_stripped

        return plate


class PlateYamlSelector(object):
    def __init__(self, yaml_dir, default_country_order=[], legacy_in_default_country_order=False):
        self.yaml_dir = yaml_dir
        self.default_country_order = default_country_order
        self.legacy_in_default_country_order = legacy_in_default_country_order
        yaml_filenames = glob.glob(os.path.join(yaml_dir, "*.yml"))
        self.schemes = {}
        for fn in yaml_filenames:
            plate_yaml = PlateYaml(fn)
            if plate_yaml.version >= 0:  # check, if loading was successful
                if plate_yaml.scheme in self.schemes:
                    self.schemes[plate_yaml.scheme][plate_yaml.version] = plate_yaml
                else:
                    self.schemes[plate_yaml.scheme] = {plate_yaml.version: plate_yaml}
        if self.schemes.get("LEGACY", {}).get(0, None) is None:
            raise Exception("NO LEGACY-0.yml")

        legacy_yaml = self.schemes["LEGACY"][0]
        del self.schemes["LEGACY"]
        if "DEFAULT" not in self.schemes:
            self.schemes["DEFAULT"] = {}

        for key in self.schemes.keys():
            self.schemes[key][0] = legacy_yaml

    def get_scheme_versions_decreasing(self, country):
        if country not in self.schemes:
            country = "DEFAULT"
        return sorted(self.schemes[country].keys(), key=lambda x: self.schemes[country][x].exactitude, reverse=True)

    def get_all_exactitudes_decreasing(self):
        exactitudes = set([])
        for s in self.schemes.keys():
            for v in self.schemes[s].keys():
                exactitudes.add(self.schemes[s][v].exactitude)
        return sorted(exactitudes, reverse=True)

    def get_best_yaml(self, scheme, version):
        if scheme not in self.schemes:
            scheme = "DEFAULT"

        versions = sorted(self.schemes.get(scheme, {}).keys(), reverse=True)
        for v in versions:
            if v <= version:
                return self.schemes[scheme][v]

        raise Exception("NO YAML FOUND! THIS SHOULD NOT HAPPEN!")

    def convert(self, plate, scheme, version, return_matched_yaml=False):
        if return_matched_yaml:
            best_yaml = self.get_best_yaml(scheme, version)
            return {"plate": best_yaml.convert(plate), "scheme": best_yaml.scheme, "version": best_yaml.version,
                    "exactitude": best_yaml.exactitude}
        else:
            return self.get_best_yaml(scheme, version).convert(plate)

    def check_ed0(self, db_cv, plate):
        if db_cv and "plate_scheme" in db_cv[0]:
            p_conv = self.convert(plate, db_cv[0]["used_scheme"], db_cv[0]["used_version"])
            for db_entry in db_cv:
                if p_conv == db_entry["plate"]:
                    return db_entry
        return None

    def check_edx(self, db_cv, plate, max_ed, ed_matches):
        if db_cv and "plate_scheme" in db_cv[0]:
            p_conv = self.convert(plate, db_cv[0]["used_scheme"], db_cv[0]["used_version"])
            for db_entry in db_cv:
                ed = editdistance.eval(p_conv, db_entry["plate"])
                if ed == 0:
                    return db_entry, ed_matches
                if ed <= max_ed and ed_matches[ed] is None:
                    ed_matches[ed] = db_entry
        return None, ed_matches

    def match_plate(self, plate, db, use_alternatives=True, max_ed=0):
        """
        Expected format of plate: {"plate": {"plate": <plate>, "confidence": <0.0-1.0>},
                                       "country": [{"country": <A/D/...>, "confidence": <0.0-1.0>}],
                                       "alternatives": [{"plate": <alt_plate1>, "confidence": <0.0-1.0>},...]}
        Expected format of db: {<Country1>: {<Version1>: [<plate1>, <plate2>,...]}}
            plates in converted form (converted using the best matching yaml, sorted into convert scheme and version,
                                                                                not db entry scheme and version)
        ED0 if use_alternatives (ed1 and alternatives does not make much sense)
        """
        max_ed = 0 if use_alternatives else max_ed
        ed_matches = [None] * (max_ed + 1)
        plates = plate.get("alternatives", []) if use_alternatives else plate.get("alternatives", [])[:1]
        for p in plates:
            check_other = False
            # first check based on countries given in plate
            checked_countries = []
            for c in plate.get("country", []):
                country = c["country"]
                if country == "OTHER":
                    check_other = True
                    break
                if country not in db:
                    continue
                for version in self.get_scheme_versions_decreasing(country):
                    if max_ed == 0:
                        res = self.check_ed0(db[country].get(version, []), p["plate"])
                        if res is not None:
                            return res
                    else:
                        res, ed_matches = self.check_edx(db[country].get(version, []), p["plate"], max_ed, ed_matches)
                        if res is not None:
                            return res
                checked_countries.append(country)

            # if other specified, check other contries
            if check_other:
                no_legacy_checked_countries = []
                # first check in order given in config, but ignoring legacy (if not legacy_in_default_country_order)
                for country in self.default_country_order:
                    if country in checked_countries or country not in db:
                        continue
                    versions = self.get_scheme_versions_decreasing(country)
                    if not self.legacy_in_default_country_order:
                        versions = versions[:-1]
                    for version in versions:
                        if max_ed == 0:
                            res = self.check_ed0(db[country].get(version, []), p["plate"])
                            if res is not None:
                                return res
                        else:
                            res, ed_matches = self.check_edx(db[country].get(version, []), p["plate"], max_ed,
                                                             ed_matches)
                            if res is not None:
                                return res
                    if self.legacy_in_default_country_order:
                        checked_countries.append(country)
                    else:
                        no_legacy_checked_countries.append(country)

                # rest is checked in decreasing version order
                for exactitude in self.get_all_exactitudes_decreasing():
                    for country, db_country in db.items():
                        if country in checked_countries or exactitude != 0 and country in no_legacy_checked_countries:
                            continue
                        for version, db_cv in db_country.items():
                            if db_cv and db_cv[0]["exactitude"] == exactitude:
                                if max_ed == 0:
                                    res = self.check_ed0(db[country].get(version, []), p["plate"])
                                    if res is not None:
                                        return res
                                else:
                                    res, ed_matches = self.check_edx(db[country].get(version, []), p["plate"], max_ed,
                                                                     ed_matches)
                                    if res is not None:
                                        return res

            for edm in ed_matches:
                if edm is not None:
                    return edm
        return None
