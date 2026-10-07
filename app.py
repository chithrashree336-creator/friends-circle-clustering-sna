from flask import Flask, render_template
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import community as community_louvain

app = Flask(__name__)

analysis_cache = None

def analyze_graph():
    file_path = 'dataset/twitter_combined.txt'

    G = nx.read_edgelist(file_path)

    partition = community_louvain.best_partition(G)
    communities = len(set(partition.values()))

    sample_nodes = list(G.nodes())[:100]
    H = G.subgraph(sample_nodes)

    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(H, seed=42)

    node_colors = [partition[node] for node in H.nodes()]

    nx.draw_networkx_nodes(
        H, pos,
        node_size=80,
        node_color=node_colors,
        cmap=plt.cm.Set3
    )

    nx.draw_networkx_edges(H, pos, alpha=0.3)

    plt.title("Friend Circle Clustering")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("static/graph.png")
    plt.close()

    return G.number_of_nodes(), G.number_of_edges(), communities


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result')
def result():
    global analysis_cache

    if analysis_cache is None:
        analysis_cache = analyze_graph()

    nodes, edges, communities = analysis_cache

    return render_template(
        'result.html',
        nodes=nodes,
        edges=edges,
        communities=communities
    )


@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run(debug=True)