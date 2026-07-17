from fpdf import FPDF
from io import BytesIO


class TravelPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, "AI Travel Planner Report", ln=True, align="C")
        self.ln(5)
        self.set_draw_color(41, 128, 185)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(44, 62, 80)
        self.ln(4)
        self.cell(0, 8, title, ln=True)
        self.set_draw_color(189, 195, 199)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_title(self, title: str):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(52, 73, 94)
        self.cell(0, 7, title, ln=True)
        self.ln(1)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        safe_text = text.encode("latin-1", "replace").decode("latin-1")
        self.multi_cell(0, 5, safe_text)
        self.ln(2)

    def bullet_point(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        safe_text = text.encode("latin-1", "replace").decode("latin-1")
        self.cell(5)
        self.cell(5, 5, chr(149))
        self.multi_cell(0, 5, safe_text)
        self.ln(1)

    def key_value(self, key: str, value: str):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(52, 73, 94)
        safe_key = key.encode("latin-1", "replace").decode("latin-1")
        self.cell(50, 5, f"{safe_key}:")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        safe_val = str(value).encode("latin-1", "replace").decode("latin-1")
        self.multi_cell(0, 5, safe_val)
        self.ln(1)

    def add_table(self, headers: list, rows: list):
        available_width = self.w - 20
        num_cols = len(headers)

        self.set_font("Helvetica", "B", 8)
        col_widths = []
        for i, h in enumerate(headers):
            max_len = len(str(h))
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(str(row[i])))
            col_widths.append(max_len)

        total_chars = sum(col_widths) or 1
        col_widths = [max((w / total_chars) * available_width, 18) for w in col_widths]
        scale = available_width / sum(col_widths)
        col_widths = [w * scale for w in col_widths]

        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            safe_h = str(h).replace("_", " ").title().encode("latin-1", "replace").decode("latin-1")
            self.cell(col_widths[i], 7, safe_h, border=1, align="C", fill=True)
        self.ln()

        self.set_font("Helvetica", "", 8)
        self.set_text_color(33, 33, 33)
        fill = False
        row_height = 6
        for row in rows:
            if fill:
                self.set_fill_color(235, 245, 251)
            else:
                self.set_fill_color(255, 255, 255)

            max_lines = 1
            cell_texts = []
            for i, cell in enumerate(row):
                safe_cell = str(cell).encode("latin-1", "replace").decode("latin-1")
                cw = col_widths[i] if i < len(col_widths) else col_widths[-1]
                char_limit = max(int(cw / 2), 10)
                if len(safe_cell) > char_limit:
                    lines = [safe_cell[j:j+char_limit] for j in range(0, len(safe_cell), char_limit)]
                    max_lines = max(max_lines, len(lines))
                    cell_texts.append("\n".join(lines))
                else:
                    cell_texts.append(safe_cell)

            cell_h = row_height * max_lines
            x_start = self.get_x()
            y_start = self.get_y()

            if y_start + cell_h > self.h - 20:
                self.add_page()
                y_start = self.get_y()

            for i, text in enumerate(cell_texts):
                cw = col_widths[i] if i < len(col_widths) else col_widths[-1]
                x = x_start + sum(col_widths[:i])
                self.set_xy(x, y_start)
                self.rect(x, y_start, cw, cell_h)
                if fill:
                    self.set_fill_color(235, 245, 251)
                    self.rect(x, y_start, cw, cell_h, "F")
                else:
                    self.set_fill_color(255, 255, 255)
                    self.rect(x, y_start, cw, cell_h, "F")
                self.rect(x, y_start, cw, cell_h, "D")
                self.set_xy(x + 1, y_start + 1)
                self.multi_cell(cw - 2, row_height, text, align="C")

            self.set_xy(x_start, y_start + cell_h)
            fill = not fill
        self.ln(3)


def _render_dict_section(pdf: TravelPDF, data: dict, indent: bool = False):
    for key, val in data.items():
        label = key.replace("_", " ").title()
        if isinstance(val, dict):
            pdf.sub_title(label)
            _render_dict_section(pdf, val, indent=True)
        elif isinstance(val, list):
            pdf.sub_title(label)
            for item in val:
                if isinstance(item, dict):
                    parts = [f"{k}: {v}" for k, v in item.items()]
                    pdf.bullet_point(", ".join(parts))
                else:
                    pdf.bullet_point(str(item))
        else:
            pdf.key_value(label, str(val))


def generate_travel_pdf(data: dict, location: str, mode: str) -> bytes:
    pdf = TravelPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Trip header
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(41, 128, 185)
    pdf.cell(0, 8, f"Destination: {location}", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Report Type: {mode}", ln=True)
    pdf.ln(5)

    # Weather
    if "current_weather" in data:
        pdf.section_title("Weather Forecast")
        cw = data["current_weather"]
        if isinstance(cw, dict):
            for k, v in cw.items():
                pdf.key_value(k.replace("_", " ").title(), str(v))
        else:
            pdf.body_text(str(cw))

        if "forecast" in data:
            pdf.sub_title("5-Day Forecast")
            forecast = data["forecast"]
            if isinstance(forecast, dict):
                for day, info in forecast.items():
                    pdf.bullet_point(f"{day}: {info}")
            elif isinstance(forecast, list):
                for item in forecast:
                    pdf.bullet_point(str(item) if not isinstance(item, dict) else ", ".join(f"{k}: {v}" for k, v in item.items()))

        if "advice" in data:
            pdf.sub_title("Travel Advice")
            pdf.body_text(data["advice"])

    # Hotels
    if "hotels" in data:
        pdf.section_title("Hotel Recommendations")
        hotels = data["hotels"]
        if isinstance(hotels, list) and hotels:
            if isinstance(hotels[0], dict):
                priority_cols = ["name", "hotel_name", "address", "rating", "estimated_total_cost",
                                 "price_level", "room_configuration", "status"]
                available_cols = [c for c in priority_cols if any(c in h for h in hotels)]
                if not available_cols:
                    available_cols = list(hotels[0].keys())[:6]
                headers = available_cols
                rows = [[str(h.get(col, "")) for col in headers] for h in hotels]
                pdf.add_table(headers, rows)
            else:
                for h in hotels:
                    pdf.bullet_point(str(h))
        if "advice" in data and "current_weather" not in data:
            pdf.sub_title("Advice")
            pdf.body_text(data["advice"])

    # Restaurants
    if "restaurants" in data:
        pdf.section_title("Restaurant Recommendations")
        restaurants = data["restaurants"]
        if isinstance(restaurants, list) and restaurants:
            if isinstance(restaurants[0], dict):
                priority_cols = ["name", "restaurant_name", "cuisine", "cuisine_type",
                                 "rating", "address", "estimated_meal_cost", "price_level"]
                available_cols = [c for c in priority_cols if any(c in r for r in restaurants)]
                if not available_cols:
                    available_cols = list(restaurants[0].keys())[:6]
                headers = available_cols
                rows = [[str(r.get(col, "")) for col in headers] for r in restaurants]
                pdf.add_table(headers, rows)
            else:
                for r in restaurants:
                    pdf.bullet_point(str(r))
        if "advice" in data and "current_weather" not in data and "hotels" not in data:
            pdf.sub_title("Advice")
            pdf.body_text(data["advice"])

    # Attractions
    if "attractions" in data:
        pdf.section_title("Attractions & Things to Do")
        attractions = data["attractions"]
        if isinstance(attractions, list):
            for i, attr in enumerate(attractions, 1):
                if isinstance(attr, dict):
                    name = attr.get("name", attr.get("title", f"Attraction {i}"))
                    pdf.sub_title(f"{i}. {name}")
                    for k, v in attr.items():
                        if k not in ("name", "title"):
                            pdf.key_value(k.replace("_", " ").title(), str(v))
                else:
                    pdf.bullet_point(f"{i}. {attr}")

        if "travel_info" in data:
            pdf.sub_title("Travel Information")
            ti = data["travel_info"]
            if isinstance(ti, dict):
                for k, v in ti.items():
                    pdf.key_value(k.replace("_", " ").title(), str(v))

    # Itinerary
    if "itinerary" in data:
        pdf.section_title("Day-by-Day Itinerary")
        itinerary = data["itinerary"]
        if isinstance(itinerary, list):
            for day_plan in itinerary:
                if isinstance(day_plan, dict):
                    day_label = day_plan.get("day", day_plan.get("title", "Day"))
                    pdf.sub_title(str(day_label))
                    for k, v in day_plan.items():
                        if k in ("day", "title"):
                            continue
                        if isinstance(v, list):
                            pdf.set_font("Helvetica", "B", 10)
                            pdf.cell(0, 5, k.replace("_", " ").title() + ":", ln=True)
                            for item in v:
                                pdf.bullet_point(str(item))
                        elif isinstance(v, dict):
                            pdf.set_font("Helvetica", "B", 10)
                            pdf.cell(0, 5, k.replace("_", " ").title() + ":", ln=True)
                            for dk, dv in v.items():
                                pdf.bullet_point(f"{dk}: {dv}")
                        else:
                            pdf.key_value(k.replace("_", " ").title(), str(v))
                    pdf.ln(3)
                else:
                    pdf.bullet_point(str(day_plan))

    # Full travel plan sections
    if "trip_summary" in data:
        pdf.section_title("Trip Summary")
        summary = data["trip_summary"]
        if isinstance(summary, dict):
            _render_dict_section(pdf, summary)
        else:
            pdf.body_text(str(summary))

    if "daily_plan" in data:
        pdf.section_title("Daily Schedule")
        daily = data["daily_plan"]
        if isinstance(daily, list):
            for day_plan in daily:
                if isinstance(day_plan, dict):
                    day_label = day_plan.get("day", day_plan.get("title", "Day"))
                    pdf.sub_title(str(day_label))
                    for k, v in day_plan.items():
                        if k in ("day", "title"):
                            continue
                        if isinstance(v, list):
                            pdf.set_font("Helvetica", "B", 10)
                            pdf.cell(0, 5, k.replace("_", " ").title() + ":", ln=True)
                            for item in v:
                                pdf.bullet_point(str(item))
                        elif isinstance(v, dict):
                            for dk, dv in v.items():
                                pdf.key_value(dk.replace("_", " ").title(), str(dv))
                        else:
                            pdf.key_value(k.replace("_", " ").title(), str(v))
                    pdf.ln(3)

    if "accommodation" in data:
        pdf.section_title("Accommodation")
        acc = data["accommodation"]
        if isinstance(acc, dict):
            _render_dict_section(pdf, acc)
        else:
            pdf.body_text(str(acc))

    if "dining_plan" in data:
        pdf.section_title("Dining Plan")
        dining = data["dining_plan"]
        if isinstance(dining, dict):
            _render_dict_section(pdf, dining)
        else:
            pdf.body_text(str(dining))

    if "budget_breakdown" in data:
        pdf.section_title("Budget Breakdown")
        budget = data["budget_breakdown"]
        if isinstance(budget, dict):
            headers = ["Category", "Amount"]
            rows = [[k.replace("_", " ").title(), str(v)] for k, v in budget.items()]
            pdf.add_table(headers, rows)
        else:
            pdf.body_text(str(budget))

    if "packing_tips" in data:
        pdf.section_title("Packing Tips")
        tips = data["packing_tips"]
        if isinstance(tips, list):
            for tip in tips:
                pdf.bullet_point(str(tip))
        else:
            pdf.body_text(str(tips))

    if "safety_advice" in data:
        pdf.section_title("Safety Advice")
        pdf.body_text(data["safety_advice"])

    output = BytesIO()
    pdf.output(output)
    return output.getvalue()
