import os.path
import sublime, sublime_plugin

class SmartGroupListener(sublime_plugin.EventListener):
	def on_load(self, view):
		window = view.window()

		rankings1 = self.rank_groups_by_extension(view, range(0, window.num_groups()))
		if len(rankings1) == 0:
			rankings1 = [(g, 0) for g in range(0, window.num_groups())]

		rankings2 = self.rank_groups_by_common_prefix(view, [r[0] for r in rankings1])

		best = max(rankings2, key=lambda r: r[1])

		window.set_view_index(view, best[0], 0)

	def rank_groups_by_extension(self, view, groups):
		rankings = [self.rank_group_by_extension(view, group) for group in groups]
		return [r for r in rankings if r[1] > 0]

	def rank_group_by_extension(self, view, group):
		window = view.window()
		count = sum(self.has_same_extension(v, view) for v in window.views_in_group(group) if v != view)
		return (group, count)

	def has_same_extension(self, v1, v2):
		return os.path.splitext(v1.file_name())[1] == os.path.splitext(v2.file_name())[1]

	def rank_groups_by_common_prefix(self, view, groups):
		rankings = [self.rank_group_by_common_prefix(view, group) for group in groups]
		return rankings

	def rank_group_by_common_prefix(self, view, group):
		window = view.window()
		filenames = [v.file_name() for v in window.views_in_group(group) if v != view] + [view.file_name()]
		prefix = os.path.commonprefix(filenames)
		return (group, len(prefix))
