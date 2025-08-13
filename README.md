# Deep Thought

Open-source deep research agent implemented with Letta.

This code will set up the Exa MCP server + add a Letta agent with deep research
capbilities.

You'll need to 

To talk to your agent, you should go to [https://app.letta.com](https://app.letta.com) and select your agent.

## ADE Instructions

The `deep-research.af` agentfile is included in this repo. Letta supports easy imports of agentfiles,
see the documentation [here](https://docs.letta.com/guides/agents/agent-file#using-agent-file-with-letta) for
more information on how to import the agent file.

**You will have to set up the Exa MCP server**. Sign up at [exa.ai](https://exa.ai) and get an API key.

After importing the agentfile, go to the Letta ADE and add the Exa MCP server.

While viewing your agent in the ADE, click Tool Manager > Add MCP Server > Exa. Paste in your Exa key.

Go wild!

## Code instructions

### Get a Letta Cloud API key

1. Go to [https://app.letta.com](https://app.letta.com)
2. Sign in or create an account
3. Skip or follow the onboarding
4. Click your profile in the top right of the ADE
5. Click "API Keys"
6. Click "Create API Key" in the top right, and provide a name for the key (this is only for you to remember the key)
7. Copy the key to a new `.env` file in this folder and assign it to the environment variable `LETTA_API_KEY`

After step 7, your `.env` file should look like this:

```bash
LETTA_API_KEY="sk-let-1235402450-923459....."
````

**Optional**: You can also self-host a Letta server.
To do so, see [the documentation](https://docs.letta.com/guides/selfhosting).

If you are using a self-hosted Letta server, uncomment and set the `LETTA_BASE_URL` variable in your `.env` file:

```bash
LETTA_BASE_URL="http://localhost:8283"  # Replace with your self-hosted server URL
```

### Get an Exa API key

This example uses [Exa](https://exa.ai) for web search and crawling.

Steps:

1. Go to [Exa](https://exa.ai) and create an account
2. Create an API key by clicking "API Keys" on the left side of the Exa dashboard
3. Copy the API key to `.env` using the environment variable `EXA_API_KEY`

Your `.env` file should look like this:

```bash
LETTA_API_KEY="sk-let-1235402450-923459....."
EXA_API_KEY="blah-blah-blah"
# LETTA_BASE_URL="http://localhost:8283"  # Only uncomment if using self-hosted Letta
```

### Install Python dependencies

We recommend using `uv` to manage Python dependencies. You can install uv [here](https://docs.astral.sh/uv/).

```bash
uv pip install -r requirements.txt
```
  
Or, if you prefer to use `pip` and ruin your life, you can use:

```bash
pip install -r requirements.txt
```

### Run the deep research script

```bash
python research.py
```

## Usage

To use the agent, 
