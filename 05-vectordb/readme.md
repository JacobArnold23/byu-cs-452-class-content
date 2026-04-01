## Introduction

Vector databases are currently widely used in industry to solve problems such as similarity and semantic search, retrieval augmented generation, image search, recommendation systems, natural language processing (NLP), and computer vision.

The basic idea is that we use some type of neural network to compress salient information found in high-dimensional data, such as large documents or images, into a fixed-size low-dimensional vector. Vectors refer to mathematical representations of data points in multidimensional space. They are typically arrays or lists of numerical values that capture an entity's essential features or attributes. In machine learning and data science, vectors encode information in a way that enables efficient computation and analysis.

Recent advances in vector databases allow us to perform linear algebra computations on vector spaces with raw SQL code. In this lab we will use pgvector, which is a PostgreSQL extension that provides powerful functionality for working with vectors in high-dimensional space. It introduces a dedicated data type, operators, and functions that enable efficient storage, manipulation, and analysis of vector data directly within the PostgreSQL database.

One of the main challenges and learning opportunities in this project will be transforming and moving data into PostgreSQL.

## Podcast Recommendation

In this lab we will build a small-scale podcast recommender system using the science and technology podcast [The Lex Fridman Podcast](https://www.youtube.com/lexfridman). Specifically, we will use GPT models from OpenAI to embed podcast segments into a vector space. We will load these vectors into a PostgreSQL database with the pgvector extension enabled. Finally, we will write queries to find similar segments and similar episodes to an input podcast segment.

## Building Your Service

In order to build our recommender system, we will use a managed PostgreSQL instance and the Python PostgreSQL client [psycopg2](https://pypi.org/project/psycopg2/).

### Dataset

We will use the open source Lex Fridman dataset hosted on Hugging Face, which contains text transcripts of recent Lex Fridman podcast episodes. The dataset consists of 346 podcasts and 832,839 podcast segments. A podcast segment is one or two sentences uttered by the same speaker.

The raw text has already been passed through the [OpenAI embeddings API](https://platform.openai.com/docs/guides/embeddings) to generate a 128-dimensional vector for each of the 832,839 podcast segments found in the dataset.

You can download:

- The raw podcast content [here](https://drive.google.com/file/d/1RXxlcUBHhE4_fQHU3qlX7Ghz5pBSvNrV/view?usp=sharing)
- The embeddings [here](https://drive.google.com/file/d/1uCx21PhPtpnmy3ZpTc8MoR0vvokTYzrB/view?usp=drive_link)
- Or use the [Colab notebook](https://colab.research.google.com/github/byu-cs-452/byu-cs-452-class-content/blob/main/embed/VectorDB_Lab_CS452_(starter).ipynb)

### Setup Your PostgreSQL Instance

You can use a 30-day free trial on TimescaleDB ([instructions](https://byu.instructure.com/courses/33212/pages/timescale-setup-instructions-2)) or use the Google Colab option that includes PostgreSQL.

### Database Schema

We will create a database with two tables: `podcast` and `segment`.

#### `podcast`

- `id` (Primary Key)
  - The unique podcast ID found in the Hugging Face data.
  - Example: `TRdL6ZzWBS0` is the ID for `Jed Buchwald: Isaac Newton and the Philosophy of Science | Lex Fridman Podcast #214`

- `title`
  - The title of the podcast.
  - Example: `Jed Buchwald: Isaac Newton and the Philosophy of Science | Lex Fridman Podcast #214`

#### `segment`

- `id` (Primary Key)
  - The unique identifier for the podcast segment.
  - This was created by concatenating the podcast index and the segment index together.
  - Example: `"0;1"` is the 0th podcast and the 1st segment.
  - This is present as the `custom_id` field in the `embedding.jsonl` and `batch_request.jsonl` files.

- `start_time`
  - The start timestamp of the segment.

- `end_time`
  - The end timestamp of the segment.

- `content`
  - The raw text transcription of the podcast.

- `embedding`
  - The 128-dimensional vector representation of the text.

- `podcast_id` (Foreign Key)
  - Foreign key to `podcast.id`

### Starter Code

**Colab Option:** [Starter notebook in Colab (includes PostgreSQL)](https://colab.research.google.com/github/byu-cs-452/byu-cs-452-class-content/blob/main/embed/VectorDB_Lab_CS452_(starter).ipynb)

**Local Option:** Dr. Jenkins provided starter code at this [GitHub repo](https://github.com/porterjenkins/byu-cs452-labs/tree/main/recommender).

Your task will be to go through each of the files in the starter code and fill in the missing `TODO` statements. The starter code is meant to provide the primary logical blocks required to complete the lab. A `requirements.txt` file is also included so you can easily install the required libraries. It is recommended that you use a conda environment for this project.

#### `db_build.py`

In this file you will implement the following major functions:

- Create the pgvector extension for PostgreSQL (code given)
- Write a `CREATE TABLE` statement for the `podcast` table
- Write a `CREATE TABLE` statement for the `segment` table
- Using the `psycopg2` Python client, create both tables

#### `db_insert.py`

In this file we will populate our database with podcast data. There are several data sources, so you will need to inspect the data from each source to determine where the fields for each table come from and create the appropriate DataFrames.

You should:

- Read the raw text data from each of the `batch_request_{XX}.jsonl` files
- Read the vector embeddings from the `embeddings.jsonl` files
- Optionally read the raw dataset from Hugging Face
- Insert all podcasts into the `podcast` table
  - The recommended way is to create a pandas DataFrame and pass it into the provided `fast_pg_insert` function.
  - This uses the `pgcopy` module of `psycopg2` and is much faster than individual inserts.
- Insert all podcast segments into the `segment` table
  - The recommended insertion method is the same as above.

Currently pgvector supports the following distance functions:

- `<->` — L2 distance
- `<#>` — negative inner product
- `<=>` — cosine distance
- `<+>` — L1 distance (added in version 0.7.0)

See the [pgvector documentation](https://github.com/pgvector/pgvector) for a full list of vector operations.

#### `db_query.py`

In this file you will write queries to answer the following questions. Use L2 distance for all queries. In each case, be sure to exclude the query document from the return list. You do not want to recommend the podcast or segment that you are querying against.

### Q1)

What are the five most similar segments to segment `"267:476"`?

Input:

```text
"that if we were to meet alien life at some point"