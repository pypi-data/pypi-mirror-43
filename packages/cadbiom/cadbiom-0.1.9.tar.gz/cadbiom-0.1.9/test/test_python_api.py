# -*- coding: utf-8 -*-
"""Unit tests for Python API"""

from __future__ import unicode_literals
from __future__ import print_function


# Standard imports
import pytest
import tempfile

@pytest.fixture()
def feed_model_with_SCC():
    """Fixture for a Cadbiom model with 4 Strongly Connected Components

    :return: A list of SCC, and the corrected model with start nodes inserted.
    :rtype: <tuple <list>, <str>>
    """

    scc = [['I', 'K', 'J', 'L'], ['Y', 'X', 'Z']]
    model = """<model xmlns="http://cadbiom" name="">
  <CSimpleNode name="A" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="B" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="E" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="D" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="C" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="Y" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="X" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="Z" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="I" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="K" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="J" xloc="0.0" yloc="0.0"/>
  <CSimpleNode name="L" xloc="0.0" yloc="0.0"/>
  <CStartNode name="__start__0" xloc="0" yloc="0"/>
  <CStartNode name="__start__1" xloc="0" yloc="0"/>
  <transition ori="I" ext="J" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="L" ext="I" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="K" ext="L" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="X" ext="Z" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="__start__1" ext="X" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="J" ext="K" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="B" ext="D" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="A" ext="B" event="" condition="C" action="" fact_ids="[]"/>
  <transition ori="X" ext="C" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="C" ext="B" event="" condition="A" action="" fact_ids="[]"/>
  <transition ori="I" ext="K" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="D" ext="C" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="J" ext="B" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="__start__0" ext="I" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="Y" ext="X" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="Z" ext="Y" event="" condition="" action="" fact_ids="[]"/>
  <transition ori="D" ext="E" event="" condition="" action="" fact_ids="[]"/>
</model>
"""

    return scc, model


def test_SCC_search(feed_model_with_SCC):
    """
    """

    import cadbiom.models.guard_transitions.analyser.model_corrections as mc

    model = feed_model_with_SCC[1]

    # Create the file model in /tmp/
    # Note: prevent the deletion of the file after the close() call
    fd_model = tempfile.NamedTemporaryFile(suffix='.bcx', delete=False)
    fd_model.write(
        """<model xmlns="http://cadbiom" name="">
    <CSimpleNode name="A"/>
    <CSimpleNode name="B"/>
    <CSimpleNode name="E"/>
    <CSimpleNode name="D"/>
    <CSimpleNode name="C"/>
    <CSimpleNode name="Y"/>
    <CSimpleNode name="X"/>
    <CSimpleNode name="Z"/>
    <CSimpleNode name="I"/>
    <CSimpleNode name="K"/>
    <CSimpleNode name="J"/>
    <CSimpleNode name="L"/>
    <transition name="" ori="A" ext="B" event="" condition="C"/>
    <transition name="" ori="B" ext="D" event="" condition=""/>
    <transition name="" ori="C" ext="B" event="" condition="A"/>
    <transition name="" ori="D" ext="C" event="" condition=""/>
    <transition name="" ori="D" ext="E" event="" condition=""/>
    <transition name="" ori="Z" ext="Y" event="" condition=""/>
    <transition name="" ori="Y" ext="X" event="" condition=""/>
    <transition name="" ori="X" ext="Z" event="" condition=""/>
    <transition name="" ori="X" ext="C" event="" condition=""/>
    <transition name="" ori="I" ext="J" event="" condition=""/>
    <transition name="" ori="L" ext="I" event="" condition=""/>
    <transition name="" ori="K" ext="L" event="" condition=""/>
    <transition name="" ori="J" ext="K" event="" condition=""/>
    <transition name="" ori="J" ext="B" event="" condition=""/>
    <transition name="" ori="I" ext="K" event="" condition=""/>
    </model>"""
    )
    fd_model.close()


    # Make a new model file (with "_without_scc" suffix in filename)
    mc.add_start_nodes(fd_model.name) # Filename + path

    with open(fd_model.name[:-4] + "_without_scc.bcx", 'r') as file:
        assert model == file.read()
