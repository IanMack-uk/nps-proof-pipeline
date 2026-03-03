from __future__ import annotations

from nps.models.graph.line_graph import line_ball
from nps.models.graph.simple_graph import SimpleGraph


def test_line_ball_triangle() -> None:
    g = SimpleGraph(n=3, edges=[(0, 1), (1, 2), (0, 2)])

    # In a triangle, every edge is adjacent to the other two.
    assert line_ball(g, 0, radius=0) == {0}
    assert line_ball(g, 0, radius=1) == {0, 1, 2}


def test_line_ball_path() -> None:
    g = SimpleGraph(n=4, edges=[(0, 1), (1, 2), (2, 3)])

    # Middle edge sees all edges at radius 1; end edge sees two.
    assert line_ball(g, 1, radius=1) == {0, 1, 2}
    assert line_ball(g, 0, radius=1) == {0, 1}


def test_line_ball_square() -> None:
    g = SimpleGraph(n=4, edges=[(0, 1), (1, 2), (2, 3), (0, 3)])

    # Each edge in a 4-cycle is adjacent to its two neighbors.
    assert line_ball(g, 0, radius=1) == {0, 1, 2}
    assert line_ball(g, 0, radius=2) == {0, 1, 2, 3}
