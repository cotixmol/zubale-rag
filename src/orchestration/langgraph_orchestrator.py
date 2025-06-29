from langgraph.graph import StateGraph, END
from src.services.interfaces import (
    RetrievalServiceInterface,
    GenerationServiceInterface,
    CallbackServiceInterface,
)
from src.models.orchestration import AgentState


class LangGraphOrchestrator:
    """
    Orchestrates the RAG flow using LangGraph to define a multi-agent system.
    """

    def __init__(
        self,
        retrieval_service: RetrievalServiceInterface,
        generation_service: GenerationServiceInterface,
        callback_service: CallbackServiceInterface,
    ):
        self.retrieval_service = retrieval_service
        self.generation_service = generation_service
        self.callback_service = callback_service
        self.workflow = self._build_graph()

    async def _retriever_node(self, state: AgentState):
        """Takes the query and finds relevant documents."""
        documents = await self.retrieval_service.find_similar_products(state.query)
        return {"documents": documents}

    def _responder_node(self, state: AgentState):
        """Takes documents and the query to generate a response."""
        response = self.generation_service.generate_response(
            state.documents, state.query
        )
        return {"response": response}

    async def _callback_node(self, state: AgentState):
        """Takes the final response and sends it to the callback URL."""
        await self.callback_service.send_response(
            user_id=state.user_id, answer=state.response
        )
        return {}

    def _build_graph(self):
        """
        Defines the flow of agents.
        """
        graph = StateGraph(AgentState)

        graph.add_node("retriever", self._retriever_node)
        graph.add_node("responder", self._responder_node)
        graph.add_node("callback", self._callback_node)

        graph.set_entry_point("retriever")
        graph.add_edge("retriever", "responder")
        graph.add_edge("responder", "callback")
        graph.add_edge("callback", END)

        return graph.compile()

    async def process_query(self, user_id: str, query: str):
        """
        Executes the full RAG and callback workflow.
        """
        inputs = {"user_id": user_id, "query": query}
        await self.workflow.ainvoke(inputs)
        print(f"Workflow complete for user {user_id}.")
