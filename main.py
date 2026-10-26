import asyncio
from dotenv import load_dotenv
import os

from langchain_core.messages import HumanMessage
from mcp import ClientSession,StdioServerParameters
#StdioServerParameters: "Come faccio ad avviare il server MCP?" equivale a uv run server.py
#ClientSession: ClientSession è l'oggetto che gestisce la comunicazione tra il tuo client e un server MCP, permettendoti di scoprire e invocare tool, risorse e prompt esposti dal server.
from mcp.client.stdio import stdio_client #client che gestisce la sessione
from langchain_mcp_adapters.tools import load_mcp_tools
#from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()



llm=ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"))
stdio_server_params=StdioServerParameters(
    command="python",
    args=["/Users/domenico.iaderosa/progetti/mcp-crash-course/servers/math_server.py"],

)

#ClientSession è il "telefono" con cui parli al server MCP, mentre session.initialize() è la chiamata iniziale che stabilisce la conversazione e verifica che client e server parlino lo stesso protocollo.
#Avvia il processo MCP descritto in stdio_server_params, apri i canali di lettura e scrittura verso il server, assegnali alle variabili read e write, e chiudi tutto automaticamente quando esco dal blocco.
async def main():
    #Avvia il server, usalo dentro il blocco e chiudilo automaticamente alla fine.
    async with stdio_client(stdio_server_params) as (read,write): #avvia il server MCP definito nei parametri (stdio_server_params) => python server.py
        #write → usato per inviare richieste al server
        #read → usato per leggere le risposte del server
        #ClientSession utilizza proprio quei due stream appena ottenuti per parlare con il server MCP.
        async with ClientSession(read_stream=read,write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            #Chiedi al server MCP quali strumenti mette a disposizione e salva la risposta nella variabile tools.
            tools= await load_mcp_tools(session)
            agent=create_agent(llm,tools) #on l'agent è invece l'LLM che decide quando e come usarli.
            result= await agent.ainvoke({"messages":[HumanMessage(content="what is 2+2?")]})
            print(result["messages"][-1].text)



if __name__=="__main__":
    asyncio.run(main())