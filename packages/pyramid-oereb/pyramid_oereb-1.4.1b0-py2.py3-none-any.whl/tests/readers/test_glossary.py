# -*- coding: utf-8 -*-
import pytest

from pyramid_oereb.lib.config import Config
from pyramid_oereb.lib.sources import Base
from pyramid_oereb.lib.readers.glossary import GlossaryReader


@pytest.mark.run(order=2)
def test_init():
    reader = GlossaryReader(
        Config.get_glossary_config().get('source').get('class'),
        **Config.get_glossary_config().get('source').get('params')
    )
    assert isinstance(reader._source_, Base)


@pytest.mark.run(order=2)
def test_read():
    reader = GlossaryReader(
        Config.get_glossary_config().get('source').get('class'),
        **Config.get_glossary_config().get('source').get('params')
    )
    results = reader.read()
    assert isinstance(results, list)
    assert len(results) == 1

# TODO: Implement tests for return values, not possible now, cause there is no data in database
