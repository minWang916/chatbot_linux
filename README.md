# Chatbot for Linux and Git Commands

***Group member***
| Name                   | Student ID |
|------------------------|------------|
| Do Minh Quang          | 10421051   |
| Le Cong Nguyen         | 10421043   |
| Duong Thien Huong      | 10421019   |

This project is a chatbot designed to assist users with Linux and Git commands. Built with the Chainlit framework and OpenAI's language models (GPT-3.5 and GPT-4), it provides an interactive and efficient way to solve technical queries.

## Features

- **Multi-Model Support**: Choose between GPT-3.5 and GPT-4 for varying levels of performance.
- **Context-Aware Responses**: Maintains conversation history for contextual interactions.
- **Knowledge Base Integration**: Uses LlamaIndex to retrieve and answer queries based on preloaded documents.
- **Cost Tracking**: Displays token usage costs to monitor API expenses.
- **Secure Authentication**:
  - Password-based authentication for predefined users.
  - OAuth support for third-party login providers.

## Installation

### Prerequisites

- Python 3.8 or above
- `pip` package manager
- OpenAI and Literal AI API keys
- Environment file (`.env`) with secret keys. Rename our `example.env` to `.env` in the root folder and replace placeholder values (e.g., `your_openai_api_key`) with your actual keys and secrets.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/minWang916/chatbot_linux.git
   cd chatbot_linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Prepare data:
   - Add relevant documents for the chatbot's knowledge base to the `data` directory.
   - Note that the documents in preparations should be short for efficient processing and accurate retrieval. Long documents may exceed the model's token limits or lead to slower query performance.

4. Run the chatbot development environment:
   ```bash
   chainlit run main.py --debug
   ```

## Usage

### Authentication

- **Password-Based Login**:
  - Admin Credentials: `admin` / `admin`
  - User Credentials: `taikhoan916` / `matkhau916`
- **OAuth Login**:
  - Login via supported third-party OAuth providers.

### Chat Interaction

- Choose your preferred model (GPT-3.5 or GPT-4) at the start of the chat.
- Ask questions about Linux or Git commands, and the chatbot will respond using its knowledge base and contextual understanding.

### Cost Tracking

The chatbot calculates and displays the token usage costs for each conversation, helping users monitor API expenses.

## Project Structure

```
chatbot_linux/
├── .chainlit/                # Configuration files for Chainlit
├── data/                     # Directory for storing documents
├── storage/                  # Persistent storage for LlamaIndex
├── auth.py                   # Handles authentication logic
├── chat.py                   # Chat handling and message processing
├── main.py                   # Entry point for the application
├── utils.py                  # Utility functions for token counting and cost tracking
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
└── LICENSE                   # Project license
```

## How It Works

1. The chatbot loads documents from the `data` directory and creates an index using LlamaIndex.
2. Users interact with the bot via Chainlit, asking questions about Linux and Git commands.
3. The chatbot queries the index or OpenAI API for responses.
4. Conversation history is maintained, with tokens tracked and costs calculated dynamically.

## Future Enhancements

- Add support for dynamic user creation.
- Improve OAuth token validation.
- Expand the knowledge base to cover more technical topics.

## Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.