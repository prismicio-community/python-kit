#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Experiments(object):

    def __init__(self, draft, running):
        self.draft = draft
        self.running = running

    def ref_from_cookie(self, cookie):
        if cookie is None:
            return None
        splitted = cookie.strip().split("%20")
        experiment = None
        if len(splitted) >= 2:
            experiment = next((exp for exp in self.running if exp.google_id == splitted[0]), None)
        if experiment is None:
            return None
        var_index = int(splitted[1])
        if -1 < var_index < len(experiment.variations):
            return experiment.variations[var_index].ref

    @staticmethod
    def parse(json):

        return Experiments(
            [Experiment.parse(e) for e in ((json and json.get("draft") or []))],
            [Experiment.parse(e) for e in ((json and json.get("running") or []))]
        )


class Experiment(object):

    def __init__(self, eid, google_id, name, variations):
        self.id = eid
        self.google_id = google_id
        self.name = name
        self.variations = variations

    @staticmethod
    def parse(json):
        return Experiment(
            json.get("id"),
            json.get("googleId"),
            json.get("name"),
            [Variation.parse(v) for v in json.get("variations")]
        )


class Variation(object):

    def __init__(self, vid, ref, label):
        self.id = vid
        self.ref = ref
        self.label = label

    @staticmethod
    def parse(json):
        return Variation(
            json.get("id"),
            json.get("ref"),
            json.get("label")
        )

