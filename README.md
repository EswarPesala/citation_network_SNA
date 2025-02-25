# citation_network_SNA
The citation network analysis of **IIT Patna** and **NIT Meghalaya** focuses on understanding the academic influence of faculty members based on their publications and citation patterns. Using **Selenium**, we extracted publication data from Google Scholar for four professors: **Arjit Mondal and Mayank Agarwal (IIT Patna)**, and **Diptendu Sinha Roy and Bunil Kumar Balabantaray (NIT Meghalaya)**. The extracted data includes publication titles and the number of times each paper has been cited.

We constructed a **directed citation network** using **NetworkX**, where nodes represent research papers, and directed edges indicate citations. Several network measures were computed to evaluate the influence of different papers:

- **Degree Centrality**: Measures the importance of papers based on the number of connections (citations).
- **Eigenvector Centrality**: Identifies influential papers that are cited by other influential papers.
- **Betweenness Centrality**: Highlights key papers that act as bridges in the citation network.
- **PageRank**: Ranks papers based on their overall influence, considering both direct and indirect citations.
- **In-degree and Out-degree Distribution**: Analyzed how citations are distributed among papers.
- **Ego-Centric Networks**: Visualized networks centered around the most influential papers.

Through **visualization techniques** such as **degree distribution plots, log-log plots, and network graphs**, we identified highly cited papers and explored the structural properties of the network. The analysis provides insights into research impact and collaboration patterns within these institutions.
