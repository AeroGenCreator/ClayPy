import flet as ft
from app_shell.container import MainContainer
from app_shell.sidebar import Sidebar
import importlib

class Shell:

	def __init__(
		self,
		page: ft.Page,
		sidebar: Sidebar,
		container: MainContainer
	):
		self.page = page
		self.sidebar = sidebar
		self.container = container
		self.construct()

	def navigate(self, route: str) -> None:
		import ipdb; ipdb.set_trace()
		module = importlib.import_module(route)
		View = getattr(module, "View", None)

		if View is None:
			raise ValueError(
				"Following path does not contain a Flet 'view'. "
				f"{module}. Make sure 'View' class exist."
			)

		view = View()
		self.view = view
		self.container = view.build()
		self.construct()

	def construct(self):
		self.page.add(
			ft.Row(
				controls=[
				self.sidebar,
				self.container
				],
				expand=True,
            	vertical_alignment=ft.CrossAxisAlignment.STRETCH
			)
		)
		self.page.update()
