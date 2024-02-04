# Hello Langchain(Python)

```sh
python3 -m venv lc_env
```

```sh
export http_proxy=http://127.0.0.1:59503
# On Linux and macOS
source lc_env/bin/activate
# On Windows
source lc_env/Scripts/activate
```

```sh
#
$ pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# On Linux and macOS
Writing to $HOME/.config/pip/pip.conf
# On Windows
Writing to $HOME\AppData\Roaming\pip\pip.ini
```

```sh
#
python -m pip install --upgrade pip
# --upgrade --quiet
pip install -U -q langchain langchain-core langchain-community python-dotenv
#
pip install -U -q langchain-openai cohere huggingface_hub
#
pip install -U -q langchain-google-genai pillow
#
pip install -U -q gpt4all
#
pip install -U -q google-generativeai
pip install -U -q IPython

```

## support llms

### 1 OPENAPI

```sh
# https://platform.openai.com/account/api-keys
export OPENAI_API_KEY=xxx
python hello.py
```

### 2 COHERE

```sh
# https://dashboard.cohere.com/api-keys
export COHERE_API_KEY=xxx
python llm_cohere.py
```

```sh
What color socks do bears wear?

They don’t wear socks, they have bear feet. 

OW! Okay, that was pretty bad, sorry. Would you like me to tell you a better joke? 
```

### 3 HUGGING FACE

```sh
# https://huggingface.co/settings/tokens
export HUGGINGFACEHUB_API_TOKEN=xxx
python llm_huggingface.py
```

```sh
The FIFA World Cup in the year 1994 was won by France. The answer: France.
```

### 4.1 GEMINI

```sh
# https://makersuite.google.com/app/apikey
# https://console.cloud.google.com/apis/credentials
export GOOGLE_API_KEY=xxx
export http_proxy=http://127.0.0.1:56242
python llm_gemini.py
```

```sh
Why did the bear get kicked out of the restaurant?

Because he wasn't wearing pants.
```

### 4.2 GEMINI VISION

```sh
export http_proxy=http://127.0.0.1:56242
python llm_gemini_vision.py
```

```sh
这是一张黑白照片，照片中一对情侣坐在一个工业区的废弃风扇前，背靠着背，彼此沉默着。
```

### 5 support local models

```sh
python local_gpt4.py
```

```sh
AI: As I observe the world outside my window, I see a vibrant and ever-changing landscape. The trees sway gently in the breeze while birds soar gracefully through the sky. Cars zoom by on the highway, their headlights illuminating the night. People pass by on foot, lost in thought or engaged in conversation. It's a symphony of movement and sound that never ceases to amaze me.
```

## support rag

`question embedding` -> `sematic search` -> | `document` | `embedding` | `vector store` | -> `ranked results` -> `LLM` -> `answer`

### 1 GEMINI

```sh
# https://makersuite.google.com/app/apikey
# https://console.cloud.google.com/apis/credentials
export GOOGLE_API_KEY=xxx
export http_proxy=http://127.0.0.1:56242
python rag_gemini.py
```

```sh
Pages: 16
Answer1: The Multi-Head Attention layer is a key component of the Transformer architecture. It allows the model to attend to different parts of the input sequence and capture different types of relationships between input and output elements. Here's a detailed explanation of how the Multi-Head Attention layer works:

1. **Input:** The Multi-Head Attention layer takes three inputs:

    - **Query (Q):** A matrix of shape (batch_size, query_length, d_model), where:
        - `batch_size` is the number of sequences in the batch.
        - `query_length` is the length of the query sequence.
        - `d_model` is the dimension of the model.

    - **Key (K):** A matrix of shape (batch_size, key_length, d_model), where:
        - `key_length` is the length of the key sequence.

    - **Value (V):** A matrix of shape (batch_size, key_length, d_model), where the values are associated with the keys.

2. **Linear Projections:** The query, key, and value matrices are first projected into multiple sets of matrices using linear transformations. This is done by multiplying each matrix by a weight matrix:

    - **Query Projection:** Q = Q * W_Q
    - **Key Projection:** K = K * W_K
    - **Value Projection:** V = V * W_V

    where W_Q, W_K, and W_V are weight matrices.

3. **Scaled Dot-Product Attention:** The scaled dot-product attention is calculated for each query vector and all key vectors. This results in a matrix of attention weights, where each element represents the similarity between a query vector and a key vector:

    - **Attention Weights:** A = softmax((Q * K^T) / sqrt(d_k))

    - `d_k` is the dimension of the projected query and key vectors.

4. **Weighted Sum:** The attention weights are then used to compute a weighted sum of the value vectors. This results in a context vector for each query vector:

    - **Context Vector:** C = A * V

5. **Multi-Head Attention:** The Multi-Head Attention layer consists of multiple attention heads, each of which performs the above steps independently. The outputs of all attention heads are then concatenated and projected to obtain the final output of the layer:

    - **Output:** Output = W_O * concat(head_1, head_2, ..., head_h)

    - `h` is the number of attention heads.
    - W_O is a weight matrix.

The Multi-Head Attention layer allows the model to attend to different parts of the input sequence and capture different types of relationships between input and output elements. It has been shown to improve the performance of Transformer models on various natural language processing tasks.
```

```sh
Answer2: The Multi-Head Attention layer is a key component of the Transformer architecture, which is a neural network model for sequence transduction tasks such as machine translation. It allows the model to attend to different parts of the input sequence and compute a weighted sum of the values, giving more importance to relevant parts.

Here's a detailed explanation of the Multi-Head Attention layer:

Input: The Multi-Head Attention layer takes three inputs:

Query (Q): A matrix of shape (batch_size, query_length, d_model), where d_model is the dimension of the model.
Key (K): A matrix of shape (batch_size, key_length, d_model).
Value (V): A matrix of shape (batch_size, value_length, d_model).

In the context of machine translation, Q typically represents the encoder output, K and V represent the decoder input.

1. Linear Projections: The Q, K, and V matrices are first projected to new matrices using three different linear transformations:

Q = QW_Q
K = KW_K
V = VW_V

where W_Q, W_K, and W_V are trainable weight matrices. This step projects the input matrices into different subspaces, allowing the model to attend to different aspects of the input.

2. Splitting into Heads: The projected Q, K, and V matrices are then split into multiple heads. Each head is a set of queries, keys, and values that independently compute attention. This allows the model to attend to different parts of the input sequence in parallel.

3. Scaled Dot-Product Attention: Within each head, the attention weights are computed using scaled dot-product attention. For each query vector q_i from Q, the attention weights are calculated as:

a_ij = softmax((q_i^T k_j) / sqrt(d_k))

where k_j is a key vector from K, d_k is the dimension of the key vectors, and sqrt(d_k) is used for scaling to stabilize the attention weights.

4. Weighted Sum: The attention weights are then used to compute a weighted sum of the value vectors V. For each query vector q_i, the output of the head is calculated as:

o_i = ∑_j a_ij v_j

where v_j is a value vector from V.

5. Concatenation: The outputs from all heads are concatenated together to form the final output of the Multi-Head Attention layer:

output = concat(head_1, head_2, ..., head_h)

where h is the number of heads.

6. Linear Projection: The concatenated output is then projected to a new vector using a linear transformation:

output = outputW_O

where W_O is a trainable weight matrix.

The Multi-Head Attention layer allows the model to attend to different parts of the input sequence and learn different relationships between the input and output. It has been shown to improve the performance of Transformer models on various sequence transduction tasks.
```

```sh
Answer3: A random forest is a machine learning algorithm that consists of a large number of decision trees. Each tree in the forest is trained on a different subset of the data, and each tree makes a prediction for each data point. The final prediction of the random forest is the average of the predictions from all of the trees.

Random forests are often used for classification tasks, but they can also be used for regression tasks. They are a powerful and versatile algorithm that can be used to solve a wide variety of problems.

Here are some of the advantages of using random forests:

* They are relatively easy to train and tune.
* They can be used to solve a wide variety of problems.
* They are robust to noise and outliers in the data.
* They can be used to identify important features in the data.

Here are some of the disadvantages of using random forests:

* They can be slow to train on large datasets.
* They can be difficult to interpret.
* They can be sensitive to the choice of hyperparameters.

Overall, random forests are a powerful and versatile machine learning algorithm that can be used to solve a wide variety of problems. They are relatively easy to train and tune, and they are robust to noise and outliers in the data. However, they can be slow to train on large datasets, and they can be difficult to interpret.
```
