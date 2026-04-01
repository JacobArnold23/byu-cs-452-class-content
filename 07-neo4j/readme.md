This assignment is a brief intro into Neo4j and how GraphDBs work. We'll start with a tutorial using a movie graph and end with the ArXiv tutorial found here:  
https://towardsdatascience.com/create-a-graph-database-in-neo4j-using-python-4172d40f89c4

**Note:** The code from the ArXiv tutorial is all in the Jupyter notebook linked below, except for the query to find the number of papers in each category. The query in the tutorial uses older and deprecated Cypher syntax. Here is the updated Cypher syntax that works (also included in the notebook):

```python
query_string = '''
MATCH (c:Category)
RETURN c.category, apoc.node.degree(c, "<IN_CATEGORY") AS inDegree
ORDER BY inDegree DESC LIMIT 20
'''

top_cat_df = pd.DataFrame([dict(_) for _ in conn.query(query_string)])
top_cat_df.head(20)
```

**Here is a notebook to help you get started:**

[neo4j_lab.ipynb](https://github.com/byu-cs-452/byu-cs-452-class-content/blob/main/notebooks/neo4j_lab.ipynb)

---

# Pass Off

Turn in a PDF file with the following:

1. **Graph of the Bacon Path for Nora Ephron using the Movies dataset**
   - A screenshot of the Neo4j Browser with the graph is sufficient.

2. **Screenshot of the inDegree vs Category Name chart**
   - From your working Jupyter notebook for the ArXiv tutorial linked above.
   - This should be a bar chart, not a graph of all the papers.

3. **Report the total number of papers from all CS categories as one total amount**
   - The query is similar to the one used in the ArXiv database tutorial but you will need to use:
     - the `WHERE` clause
     - the `STARTS WITH` operator
     - either the `count()` or the `sum()` aggregation (possibly `DISTINCT`)

4. **The query used** to get the total number of papers in all CS categories from #3
   - Explain whether you:
     - wrote a query counting all unique papers in CS categories, or
     - wrote a query that counts a paper once for each CS category it participates in.
   - Either approach is acceptable; just explain which one you used.
   - Optionally, try the other approach as well for comparison.

5. **Experiment with the technology**
   - Do something interesting or run a query you find meaningful.