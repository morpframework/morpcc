import itertools
import json

from .base import Widget

default_color_stack = ["#455C73", "#9B59B6", "#26B99A", "#3498DB", "#BDC3C7"]


class TileStatsCount(Widget):
    """
        Requires row to have 'tile_count' class
    """

    template = "master/dashboard/tile_stats_count.pt"
    widget_css_class = "tile_stats_count"

    default_opts = {
        "xs_size": 6,
        "sm_size": 4,
        "md_size": 2,
        "lg_size": 2,
        "xl_size": 2,
    }

    def __init__(
        self,
        datasource,
        *,
        title=None,
        increment_from="Period",
        icon="database",
        value_col="value",
        increment_col="increment",
        increment_unit="%",
        **kwargs
    ):
        self.title = title
        self.increment_from = increment_from
        self.value_col = value_col
        self.increment_col = increment_col
        self.increment_unit = increment_unit
        self.icon = icon
        super().__init__(datasource, **kwargs)

    def chart_data(self, data):
        increment = data[0][self.increment_col]
        increment_icon = None
        if increment > 0:
            increment_icon = "sort-asc"
        if increment < 0:
            increment_icon = "sort-desc"
        return {
            "value": data[0][self.value_col],
            "increment": abs(increment),
            "increment_icon": increment_icon,
        }


class PercentChart(Widget):

    template = "master/dashboard/percent_chart.pt"

    default_opts = {"sm_size": 4, "md_size": 4, "lg_size": 4}

    def __init__(
        self,
        datasource,
        *,
        title=None,
        limit=10,
        label_col="label",
        value_col="value",
        total_col="total",
        **kwargs
    ):
        self.title = title
        self.limit = limit
        self.label_col = label_col
        self.value_col = value_col
        self.total_col = total_col
        super().__init__(datasource, **kwargs)

    def chart_data(self, data):
        result = []
        for r in data:
            value = r[self.value_col]
            total = r[self.total_col]
            row = {
                "label": r[self.label_col],
                "value_percent": int((value / total) * 100),
                "value_short": self.human_value(value),
            }
            result.append(row)
        return result

    def human_value(self, value):
        if value > 10 ** 12:
            return "%sT" % int(value / (10 ** 12))
        if value > 10 ** 9:
            return "%sB" % int(value / (10 ** 9))
        if value > 10 ** 6:
            return "%sM" % int(value / (10 ** 6))
        if value > 10 ** 3:
            return "%sK" % int(value / (10 ** 3))
        return "%s" % value


class ChartJS(Widget):

    template = "master/dashboard/chartjs.pt"

    def __init__(
        self,
        datasource,
        *,
        title=None,
        title_small=None,
        canvas_height=80,
        label_col="label",
        value_col="value",
        **kwargs
    ):
        self.title = title
        self.title_small = title_small
        self.canvas_height = canvas_height
        self.label_col = label_col
        self.value_col = value_col
        super().__init__(datasource, **kwargs)

    def render_script(self, context, request, load_template):
        source = self.get_datasource(request)
        chart_config = self.chart_config(source.compute())
        chart_config["responsive"] = True
        chart_config["maintainAspectRatio"] = False
        script = """
        <script>
            $(document).ready(function () { 
                var ctx = document.getElementById("%s");
                var chart = new Chart(ctx, %s)
            })
        </script>
        """ % (
            self.widget_id,
            json.dumps(chart_config),
        )
        return script

    def chart_config(self, data):
        raise NotImplementedError()


class PieChart(ChartJS):
    def __init__(self, datasource, *, max_items=4, **kwargs):
        self.max_items = max_items
        super().__init__(datasource, **kwargs)

    def chart_data(self, data):
        labels = []
        bgcolors = []
        hovcolors = []
        chart_data = []
        max_items = self.max_items
        for idx, row in enumerate(sorted(data, key=lambda x: x[self.value_col])):

            cidx = idx % len(default_color_stack)
            default_color = default_color_stack[cidx]
            if idx < max_items:
                labels.append(row[self.label_col])
                color = row.get("color", default_color)
                hover_color = row.get("hover_color", color)
                bgcolors.append(color)
                hovcolors.append(hover_color)
                chart_data.append(row[self.value_col])
            else:
                if "Others" not in labels:
                    labels.append("Others")
                if len(chart_data) <= max_items:
                    chart_data.append(0)
                    bgcolors.append(default_color)
                    hovcolors.append(default_color)
                chart_data[-1] += row[self.value_col]

        return {
            "labels": labels,
            "datasets": [
                {
                    "data": chart_data,
                    "backgroundColor": bgcolors,
                    "hoverBackgroundColor": hovcolors,
                }
            ],
        }

    def chart_config(self, data):
        return {
            "type": "pie",
            "tooltipFillColor": "rgba(51, 51, 51, 0.55)",
            "data": self.chart_data(data),
            "options": {"legend": {"position": "right"}},
        }


class DoughnutChart(PieChart):
    def chart_config(self, data):
        result = super().chart_config(data)
        result["type"] = "doughnut"
        return result


class LineChart(ChartJS):

    default_opts = {"sm_size": 12, "md_size": 12, "lg_size": 12}

    def __init__(self, datasource, *, series_col=None, default_label="Count", **kwargs):
        self.series_col = series_col
        self.default_label = default_label
        super().__init__(datasource, **kwargs)

    def chart_data(self, data):
        series_data = {}
        labels = []
        for row in data:
            if row["label"] not in labels:
                labels.append(row[self.label_col])
            if self.series:
                series_key = row[self.series_col]
            else:
                series_key = None
            series_data.setdefault(series_key, [])
            series_data[series_key].append(row[self.value_col])

        datasets = []
        for idx, r in sorted(enumerate(series_data.items()), key=lambda x: x[1][0]):
            ds = {}
            k, v = r
            cidx = idx % len(default_color_stack)
            default_color = default_color_stack[cidx]
            if k:
                ds["label"] = k
            else:
                ds["label"] = self.default_label
            ds["borderColor"] = default_color
            ds["data"] = v
            datasets.append(ds)
        return {"labels": labels, "datasets": datasets}

    def chart_config(self, data):
        data = self.chart_data(data)
        return {"type": "line", "data": data}
