from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_publications(scholar_url):
    driver.get(scholar_url)
    time.sleep(5)  # Allow page to load

    publications = []
    
    for entry in driver.find_elements(By.CSS_SELECTOR, "#gsc_a_b .gsc_a_tr"):
        try:
            title = entry.find_element(By.CSS_SELECTOR, ".gsc_a_at").text
            cited_by_elem = entry.find_element(By.CSS_SELECTOR, ".gsc_a_ac")
            cited_by = cited_by_elem.text if cited_by_elem.text else "0"
            publications.append((title, int(cited_by)))
        except Exception as e:
            print("Error:", e)
            continue
    
    return publications

# Scholar profile URLs
mayank_url = "https://scholar.google.co.in/citations?user=6Rzu0kMAAAAJ&hl=en"
arijit_url = "https://scholar.google.com/citations?user=vAY9ddAAAAAJ&hl=en"

# Extract publications
mayank_pubs = get_publications(mayank_url)
arijit_pubs = get_publications(arijit_url)

driver.quit()  # Close the browser

# Create DataFrame
data = pd.DataFrame(mayank_pubs + arijit_pubs, columns=["Title", "Cited By"])

# Construct Citation Network
G = nx.DiGraph()
for _, row in data.iterrows():
    paper = row["Title"]
    cited_by = row["Cited By"]
    G.add_node(paper)
    if cited_by > 0:
        G.add_edge(f"Cited {cited_by} times", paper)

# Compute Centrality Measures
degree_cent = nx.degree_centrality(G)
eigen_cent = nx.eigenvector_centrality(G, max_iter=1000)  # Eigenvector Centrality
betweenness_cent = nx.betweenness_centrality(G)
pagerank = nx.pagerank(G)

# Compute in-degree and out-degree distributions
in_degrees = [G.in_degree(n) for n in G.nodes()]
out_degrees = [G.out_degree(n) for n in G.nodes()]

# Compute Graph Properties
avg_in_degree = np.mean(in_degrees)
avg_out_degree = np.mean(out_degrees)


# Display Results
print("\nTop 5 Degree Centrality:")
print(dict(sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]))

print("\nTop 5 Eigenvector Centrality:")
print(dict(sorted(eigen_cent.items(), key=lambda x: x[1], reverse=True)[:5]))

print("\nTop 5 Betweenness Centrality:")
print(dict(sorted(betweenness_cent.items(), key=lambda x: x[1], reverse=True)[:5]))

print("\nTop 5 Influential Papers (PageRank):")
print(dict(sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]))

print(f"\nAverage In-degree: {avg_in_degree}")
print(f"Average Out-degree: {avg_out_degree}")

# Graph Visualization
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.15, seed=42)
nx.draw(G, pos, node_size=500, node_color="red", edge_color="black", with_labels=True, font_size=8)
plt.title("Citation Network of Mayank Agarwal & Arijit Mondal", fontsize=16, fontweight='bold')
plt.show()

# In-degree Distribution Plot
plt.figure(figsize=(8, 6))
plt.hist(in_degrees, bins=20, color="blue", alpha=0.7)
plt.xlabel("In-degree")
plt.ylabel("Frequency")
plt.title("In-degree Distribution")
plt.show()

# Out-degree Distribution Plot
plt.figure(figsize=(8, 6))
plt.hist(out_degrees, bins=20, color="green", alpha=0.7)
plt.xlabel("Out-degree")
plt.ylabel("Frequency")
plt.title("Out-degree Distribution")
plt.show()

# Log-Log Distribution of In-degree
plt.figure(figsize=(8, 6))
plt.loglog(sorted(in_degrees, reverse=True), 'bo-')
plt.xlabel("Rank")
plt.ylabel("In-degree")
plt.title("Log-Log Distribution of In-degree")
plt.show()

# Log-Log Distribution of Out-degree
plt.figure(figsize=(8, 6))
plt.loglog(sorted(out_degrees, reverse=True), 'go-')
plt.xlabel("Rank")
plt.ylabel("Out-degree")
plt.title("Log-Log Distribution of Out-degree")
plt.show()

# Ego-centric Network (for top paper)
top_paper = max(degree_cent, key=degree_cent.get)
ego_graph = nx.ego_graph(G, top_paper)

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(ego_graph, seed=42)
nx.draw(ego_graph, pos, with_labels=True, node_color="orange", edge_color="gray", node_size=700, font_size=9)
plt.title(f"Ego-Centric Network of '{top_paper}'")
plt.show()
