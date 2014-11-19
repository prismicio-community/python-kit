#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Experiments(object):
    """
    Holds informations about current experiments

    :ivar array<Experiment> running: list of currently running experiments
    :ivar array<Experiment> draft: list of drafts
    """

    def __init__(self, draft, running):
        self.draft = draft
        self.running = running

    def ref_from_cookie(self, cookie):
        """
        From a cookie set by the Prismic.io toolbar, identify the corresponding reference.

        :param cookie: the cookie set by the Prismic.io toolbar and received from the request.
        :return: the reference. May be None if it can't be found.
        """
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

    def current(self):
        """
        :return: the currently running experiment, or None
        """
        try:
            return self.running[0]
        except IndexError:
            return None

    @staticmethod
    def parse(json):

        return Experiments(
            [Experiment.parse(e) for e in ((json and json.get("draft") or []))],
            [Experiment.parse(e) for e in ((json and json.get("running") or []))]
        )


class Experiment(object):
    """
    Represents an experiment

    :ivar str id:
    :ivar str google_id:
    :ivar str name:
    :ivar array<Variation> variations:
    """

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
    """
    Represents a variation of an experiment

    :ivar str id:
    :ivar str ref:
    :ivar str label:
    """

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

