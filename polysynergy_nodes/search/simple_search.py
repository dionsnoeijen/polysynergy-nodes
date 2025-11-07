"""Simple working search node using ddgs library directly"""
from ddgs import DDGS

from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_node_runner.setup_context.path_settings import PathSettings
from polysynergy_node_runner.setup_context.node_error import NodeError


@node(
    name="Simple Search",
    category="search",
    icon="search.svg",
)
class SimpleSearch(Node):
    """
    A simple, working search node that uses DuckDuckGo directly.
    No wrappers, no complications - just search that works.
    """

    query: str = NodeVariableSettings(
        label="Query",
        dock=True,
        has_in=True,
        required=True,
        info="Search query (e.g., 'SWIS kubernetes')"
    )

    max_results: int = NodeVariableSettings(
        label="Max Results",
        dock=True,
        default=5,
        info="Maximum number of search results to return"
    )

    region: str = NodeVariableSettings(
        label="Region",
        dock=True,
        default="wt-wt",
        info="Region for search (e.g., 'nl-nl' for Netherlands, 'wt-wt' for worldwide)"
    )

    # Output
    results: list = NodeVariableSettings(
        label="Results",
        has_out=True,
        info="List of search results"
    )

    formatted_results: str = NodeVariableSettings(
        label="Formatted Results",
        has_out=True,
        info="Formatted string of all results"
    )

    true_path: bool | list = PathSettings(label="Success")
    false_path: bool | dict = PathSettings(label="Error")

    async def execute(self):
        try:
            print(f"\n[SimpleSearch] Searching for: {self.query}")
            print(f"[SimpleSearch] Max results: {self.max_results}")
            print(f"[SimpleSearch] Region: {self.region}")

            # Create DDGS instance
            ddgs = DDGS()

            # Perform search
            search_results = list(ddgs.text(
                self.query,
                region=self.region,
                max_results=self.max_results
            ))

            print(f"[SimpleSearch] Found {len(search_results)} results")

            if not search_results:
                self.results = []
                self.formatted_results = "No results found"
                self.true_path = []
                self.false_path = False
                return

            # Format results
            formatted_list = []
            clean_results = []

            for i, result in enumerate(search_results, 1):
                title = result.get('title', 'No title')
                url = result.get('href', 'No URL')
                body = result.get('body', 'No description')

                clean_results.append({
                    'title': title,
                    'url': url,
                    'description': body
                })

                formatted_list.append(
                    f"{i}. {title}\n"
                    f"   URL: {url}\n"
                    f"   {body[:150]}{'...' if len(body) > 150 else ''}"
                )

            self.results = clean_results
            self.formatted_results = "\n\n".join(formatted_list)
            self.true_path = clean_results
            self.false_path = False

            print(f"[SimpleSearch] ✓ Successfully returned {len(clean_results)} results")

        except Exception as e:
            print(f"[SimpleSearch] ✗ Error: {e}")
            self.results = []
            self.formatted_results = f"Error: {str(e)}"
            self.false_path = NodeError.format(e)
            self.true_path = False
