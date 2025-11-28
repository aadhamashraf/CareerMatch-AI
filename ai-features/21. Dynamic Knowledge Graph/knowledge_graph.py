"""Dynamic Knowledge Graph utilities (Feature 21).

Provides small helpers to construct a graph of skills, courses and projects
and to query it. This mirrors the notebook content and is import-safe.
"""
from typing import Any, Dict, List

try:
    import networkx as nx
except Exception:  # pragma: no cover - environment may not have networkx
    nx = None


def build_sample_graph():
    if nx is None:
        raise RuntimeError('networkx is required to build a knowledge graph')

    G = nx.Graph()

    # Add Skill nodes
    skills = ["Python", "Pandas", "Numpy", "SQL", "Matplotlib"]
    for s in skills:
        G.add_node(s, type='skill')

    # Courses
    courses = {
        'C1': 'Intro to Python',
        'C2': 'Data Analysis with Pandas',
        'C3': 'Database Fundamentals',
        'C4': 'Data Visualization'
    }
    for c_id, name in courses.items():
        G.add_node(c_id, type='course', name=name)

    # Projects
    projects = {
        'P1': 'Basic Web Scraper',
        'P2': 'Sales Data Analysis',
        'P3': 'Employee Database Query'
    }
    for p_id, name in projects.items():
        G.add_node(p_id, type='project', name=name)

    # edges (teaches / requires)
    G.add_edge('C1', 'Python', rel='teaches')
    G.add_edge('C2', 'Pandas', rel='teaches')
    G.add_edge('C2', 'Numpy', rel='teaches')
    G.add_edge('C2', 'Python', rel='teaches')
    G.add_edge('C3', 'SQL', rel='teaches')
    G.add_edge('C4', 'Matplotlib', rel='teaches')
    G.add_edge('C4', 'Pandas', rel='teaches')
    G.add_edge('P1', 'Python', rel='requires')
    G.add_edge('P2', 'Python', rel='requires')

    return G


def courses_teaching_skill(G, skill: str) -> List[Dict[str, Any]]:
    """Return list of course nodes that teach `skill` as dicts."""
    out = []
    for nbr in G.neighbors(skill):
        if G.nodes[nbr].get('type') == 'course' and G.edges[skill, nbr].get('rel') == 'teaches':
            out.append({'id': nbr, 'name': G.nodes[nbr].get('name')})
    return out


def projects_requiring_skill(G, skill: str) -> List[Dict[str, Any]]:
    out = []
    for nbr in G.neighbors(skill):
        if G.nodes[nbr].get('type') == 'project' and G.edges[nbr, skill].get('rel') == 'requires':
            out.append({'id': nbr, 'name': G.nodes[nbr].get('name')})
    return out


if __name__ == '__main__':
    print('Demo: building a tiny knowledge graph...')
    G = build_sample_graph()
    print('Courses teaching Pandas:', courses_teaching_skill(G, 'Pandas'))
    print('Projects requiring Python:', projects_requiring_skill(G, 'Python'))
