import streamlit as st
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pdf_generator import generate_travel_pdf

st.set_page_config(
    page_title="AI Travel Planner",
    layout="wide",
)   

API_BASE_URL = "http://localhost:8000"  # Ensure this matches your backend server URLtt


def call_api(endpoint: str, payload: dict) -> dict:
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend API. Make sure the server is running on port 8000.")
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. The agents are taking too long to respond.")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.status_code} - {e.response.text}")
        return None


def _parse_stringified(val):
    """Try to parse a string that looks like JSON/Python literal into a real object."""
    if isinstance(val, str) and val.strip().startswith(("[", "{")):
        try:
            import ast
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            try:
                return json.loads(val)
            except (ValueError, json.JSONDecodeError):
                pass
    return val


def _render_unknown_data(data: dict, skip_keys: list = None):
    """Fallback renderer for any dict data that doesn't match expected structure.
    Displays as organized key-value pairs, tables for lists of dicts, or bullet lists."""
    skip_keys = skip_keys or []
    for key, val in data.items():
        if key in skip_keys:
            continue
        label = key.replace("_", " ").title()
        val = _parse_stringified(val)

        if isinstance(val, list) and val:
            if isinstance(val[0], dict):
                st.markdown(f"**{label}:**")
                df = pd.DataFrame(val)
                df.columns = [c.replace("_", " ").title() for c in df.columns]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.markdown(f"**{label}:**")
                for item in val:
                    st.markdown(f"  - {item}")
        elif isinstance(val, dict):
            st.markdown(f"**{label}:**")
            for k, v in val.items():
                if isinstance(v, (dict, list)):
                    st.markdown(f"  - **{k.replace('_', ' ').title()}:** {v}")
                else:
                    st.markdown(f"  - **{k.replace('_', ' ').title()}:** {v}")
        elif isinstance(val, str) and len(val) > 200:
            st.markdown(f"**{label}:**")
            st.markdown(val)
        else:
            st.markdown(f"**{label}:** {val}")


def render_weather(data: dict):
    st.subheader("Weather Forecast")

    cw = data.get("current_weather", {})
    forecast = data.get("forecast", None)

    # Handle case where forecast is nested inside current_weather
    if isinstance(cw, dict) and "forecast" in cw and forecast is None:
        forecast = cw.pop("forecast", None)

    if isinstance(cw, dict) and cw:
        # Only display simple scalar values as metrics
        scalar_keys = [k for k, v in cw.items() if isinstance(v, (str, int, float))]
        if scalar_keys:
            cols = st.columns(min(len(scalar_keys), 4))
            priority_keys = ["city", "location", "temperature", "condition", "description", "humidity"]
            ordered = [k for k in priority_keys if k in scalar_keys] + [k for k in scalar_keys if k not in priority_keys]
            for i, key in enumerate(ordered):
                cols[i % len(cols)].metric(key.replace("_", " ").title(), str(cw[key]))
    elif isinstance(cw, str):
        st.markdown(cw)

    if forecast is None:
        forecast = data.get("forecast", None)

    # Parse stringified list/dict if agent returned it as a string
    if isinstance(forecast, str):
        try:
            import ast
            forecast = ast.literal_eval(forecast)
        except (ValueError, SyntaxError):
            pass

    if forecast:
        st.markdown("---")
        st.markdown("### 5-Day Forecast")

        if isinstance(forecast, list) and forecast:
            df_data = []
            for item in forecast:
                if isinstance(item, dict):
                    date_val = item.get("date", item.get("day", item.get("datetime", "")))
                    temp_str = str(item.get("temperature", item.get("temp", item.get("avg_temp", ""))))
                    condition = item.get("condition", item.get("description", item.get("weather", item.get("summary", ""))))
                    humidity = item.get("humidity", "")
                    wind = item.get("wind", item.get("wind_speed", ""))
                    temp_val = None
                    for part in temp_str.replace("°C", "").replace("°F", "").replace("°", "").split():
                        try:
                            temp_val = float(part)
                            break
                        except ValueError:
                            continue
                    row_data = {
                        "Date": str(date_val),
                        "Temperature": temp_str,
                        "Condition": str(condition),
                        "temp_numeric": temp_val,
                    }
                    if humidity:
                        row_data["Humidity"] = str(humidity)
                    if wind:
                        row_data["Wind"] = str(wind)
                    df_data.append(row_data)
                elif isinstance(item, str):
                    df_data.append({"Date": "", "Temperature": "", "Condition": item, "temp_numeric": None})

            if df_data and any(row.get("Date") or row.get("Condition") for row in df_data):
                cols_forecast = st.columns(min(len(df_data), 5))
                for i, row in enumerate(df_data):
                    with cols_forecast[i % min(len(df_data), 5)]:
                        condition = row["Condition"].lower()
                        icon = "☀️"
                        if "rain" in condition or "shower" in condition:
                            icon = "🌧️"
                        elif "thunder" in condition or "storm" in condition:
                            icon = "⛈️"
                        elif "cloud" in condition or "overcast" in condition:
                            icon = "☁️"
                        elif "partly" in condition or "partial" in condition:
                            icon = "⛅"
                        elif "snow" in condition:
                            icon = "🌨️"
                        elif "fog" in condition or "mist" in condition:
                            icon = "🌫️"
                        st.markdown(f"**{row['Date']}**")
                        st.markdown(f"### {icon}")
                        st.markdown(f"**{row['Temperature']}**")
                        st.markdown(f"{row['Condition']}")
                        if row.get("Humidity"):
                            st.caption(f"Humidity: {row['Humidity']}")
                        if row.get("Wind"):
                            st.caption(f"Wind: {row['Wind']}")

                st.markdown("#### Forecast Details")
                table_cols = ["Date", "Temperature", "Condition"]
                if any(r.get("Humidity") for r in df_data):
                    table_cols.append("Humidity")
                if any(r.get("Wind") for r in df_data):
                    table_cols.append("Wind")
                table_df = pd.DataFrame([{col: row.get(col, "") for col in table_cols} for row in df_data])
                st.dataframe(table_df, use_container_width=True, hide_index=True)

                if any(r["temp_numeric"] is not None for r in df_data):
                    chart_df = pd.DataFrame([
                        {"Date": r["Date"], "Temperature (°C)": r["temp_numeric"]}
                        for r in df_data if r["temp_numeric"] is not None
                    ])
                    fig = px.line(
                        chart_df, x="Date", y="Temperature (°C)",
                        title="Temperature Trend",
                        markers=True,
                    )
                    fig.update_layout(hovermode="x unified")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.dataframe(pd.DataFrame(forecast), use_container_width=True, hide_index=True)

        elif isinstance(forecast, dict):
            table_rows = []
            for day, info in forecast.items():
                if isinstance(info, dict):
                    row = {"Date": day}
                    row.update({k.replace("_", " ").title(): str(v) for k, v in info.items()})
                    table_rows.append(row)
                else:
                    table_rows.append({"Date": day, "Details": str(info)})
            if table_rows:
                st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        elif isinstance(forecast, str):
            st.markdown(forecast)

    if "advice" in data:
        st.markdown("---")
        st.markdown("### 🧳 Travel Advice")
        st.info(data["advice"])


def render_hotels(data: dict):
    st.subheader("🏨 Hotel Recommendations")
    hotels = data.get("hotels", [])

    if isinstance(hotels, str):
        try:
            import ast
            hotels = ast.literal_eval(hotels)
        except (ValueError, SyntaxError):
            st.markdown(hotels)
            hotels = []

    if isinstance(hotels, list) and hotels:
        if isinstance(hotels[0], dict):
            table_cols = ["name", "hotel_name", "address", "rating", "user_rating",
                         "estimated_total_cost", "estimated_cost", "price_level",
                         "room_configuration", "status", "popularity", "type"]
            available_cols = [c for c in table_cols if any(c in h for h in hotels)]
            if not available_cols:
                available_cols = list(hotels[0].keys())

            table_data = []
            for h in hotels:
                row = {}
                for col in available_cols:
                    val = h.get(col, "")
                    if isinstance(val, (dict, list)):
                        val = str(val)
                    row[col.replace("_", " ").title()] = val
                table_data.append(row)

            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### Detailed View")
        for i, hotel in enumerate(hotels, 1):
            if isinstance(hotel, dict):
                name = hotel.get("name", hotel.get("hotel_name", f"Hotel {i}"))
                rating = hotel.get("rating", hotel.get("user_rating", 0))
                try:
                    stars = "⭐" * int(float(rating))
                except (ValueError, TypeError):
                    stars = ""
                with st.expander(f"{i}. {name} {stars}", expanded=(i <= 3)):
                    col1, col2 = st.columns(2)
                    display_keys_col1 = ["address", "location", "rating", "user_rating"]
                    display_keys_col2 = ["price_level", "estimated_total_cost", "estimated_cost", "status", "room_configuration", "type", "popularity"]
                    for key in display_keys_col1:
                        if key in hotel:
                            col1.markdown(f"**{key.replace('_', ' ').title()}:** {hotel[key]}")
                    for key in display_keys_col2:
                        if key in hotel:
                            col2.markdown(f"**{key.replace('_', ' ').title()}:** {hotel[key]}")
                    other_keys = [k for k in hotel if k not in ["name", "hotel_name"] + display_keys_col1 + display_keys_col2]
                    for key in other_keys:
                        val = hotel[key]
                        if isinstance(val, list):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for item in val:
                                st.markdown(f"  - {item}")
                        elif isinstance(val, dict):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for k, v in val.items():
                                st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {val}")
            elif isinstance(hotel, str):
                st.markdown(f"{i}. {hotel}")
    elif not hotels:
        _render_unknown_data(data, skip_keys=["advice"])

    if "advice" in data:
        st.markdown("---")
        st.markdown("### 💡 Recommendation")
        st.info(data["advice"])


def render_restaurants(data: dict):
    st.subheader("🍽️ Restaurant Recommendations")
    restaurants = data.get("restaurants", [])

    if isinstance(restaurants, str):
        restaurants = _parse_stringified(restaurants)
        if isinstance(restaurants, str):
            st.markdown(restaurants)
            restaurants = []

    if isinstance(restaurants, list) and restaurants:
        if isinstance(restaurants[0], dict):
            table_cols = ["name", "restaurant_name", "cuisine", "cuisine_type", "address",
                         "rating", "user_rating", "estimated_meal_cost", "estimated_cost",
                         "price_level", "popularity", "status", "dietary_options", "type"]
            available_cols = [c for c in table_cols if any(c in r for r in restaurants)]
            if not available_cols:
                available_cols = list(restaurants[0].keys())

            table_data = []
            for r in restaurants:
                row = {}
                for col in available_cols:
                    val = r.get(col, "")
                    if isinstance(val, (dict, list)):
                        val = ", ".join(str(x) for x in val) if isinstance(val, list) else str(val)
                    row[col.replace("_", " ").title()] = val
                table_data.append(row)

            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### Detailed View")
        for i, rest in enumerate(restaurants, 1):
            if isinstance(rest, dict):
                name = rest.get("name", rest.get("restaurant_name", f"Restaurant {i}"))
                rating = rest.get("rating", rest.get("user_rating", 0))
                try:
                    stars = "⭐" * int(float(rating))
                except (ValueError, TypeError):
                    stars = ""
                with st.expander(f"{i}. {name} {stars}", expanded=(i <= 3)):
                    col1, col2 = st.columns(2)
                    left_keys = ["address", "location", "rating", "user_rating", "cuisine", "cuisine_type", "type"]
                    right_keys = ["price_level", "estimated_meal_cost", "estimated_cost", "popularity", "status", "dietary_options"]
                    for key in left_keys:
                        if key in rest:
                            col1.markdown(f"**{key.replace('_', ' ').title()}:** {rest[key]}")
                    for key in right_keys:
                        if key in rest:
                            col2.markdown(f"**{key.replace('_', ' ').title()}:** {rest[key]}")
                    other_keys = [k for k in rest if k not in ["name", "restaurant_name"] + left_keys + right_keys]
                    for key in other_keys:
                        val = rest[key]
                        if isinstance(val, list):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for item in val:
                                st.markdown(f"  - {item}")
                        elif isinstance(val, dict):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for k, v in val.items():
                                st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {val}")
            elif isinstance(rest, str):
                st.markdown(f"{i}. {rest}")
    elif not restaurants:
        _render_unknown_data(data, skip_keys=["advice"])

    if "advice" in data:
        st.markdown("---")
        st.markdown("### 💡 Recommendation")
        st.info(data["advice"])


def render_attractions(data: dict):
    st.subheader("🎯 Attractions & Things to Do")
    if "attractions" in data and isinstance(data["attractions"], list):
        for i, attr in enumerate(data["attractions"], 1):
            if isinstance(attr, dict):
                name = attr.get("name", attr.get("title", attr.get("attraction", f"Attraction {i}")))
                with st.expander(f"{i}. {name}", expanded=(i <= 5)):
                    if "description" in attr:
                        st.markdown(attr["description"])
                    col1, col2 = st.columns(2)
                    left_keys = ["location", "address", "intensity", "intensity_level", "suitability"]
                    right_keys = ["estimated_cost", "duration", "best_time", "rating"]
                    for key in left_keys:
                        if key in attr:
                            col1.markdown(f"**{key.replace('_', ' ').title()}:** {attr[key]}")
                    for key in right_keys:
                        if key in attr:
                            col2.markdown(f"**{key.replace('_', ' ').title()}:** {attr[key]}")
                    if "activities" in attr:
                        activities = attr["activities"]
                        st.markdown("**Activities:**")
                        if isinstance(activities, list):
                            for act in activities:
                                st.markdown(f"  - {act}")
                        else:
                            st.markdown(f"  {activities}")
                    other_keys = [k for k in attr if k not in ["name", "title", "attraction", "description", "activities"] + left_keys + right_keys]
                    for key in other_keys:
                        val = attr[key]
                        if isinstance(val, list):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for item in val:
                                st.markdown(f"  - {item}")
                        elif isinstance(val, dict):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for k, v in val.items():
                                st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {val}")
            elif isinstance(attr, str):
                st.markdown(f"{i}. {attr}")

    if "travel_info" in data:
        st.markdown("---")
        st.markdown("### 🚗 Travel Information")
        ti = data["travel_info"]
        if isinstance(ti, dict):
            for key, val in ti.items():
                if isinstance(val, list):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    for item in val:
                        st.markdown(f"  - {item}")
                elif isinstance(val, dict):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    for k, v in val.items():
                        st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                else:
                    st.markdown(f"- **{key.replace('_', ' ').title()}:** {val}")
        elif isinstance(ti, str):
            st.markdown(ti)


def render_itinerary(data: dict):
    st.subheader("📅 Day-by-Day Itinerary")
    if "itinerary" in data and isinstance(data["itinerary"], list):
        cost_data = []
        for day_plan in data["itinerary"]:
            if isinstance(day_plan, dict):
                day_num = day_plan.get("day", day_plan.get("title", "Day"))
                day_label = f"Day {day_num}" if isinstance(day_num, int) else str(day_num)
                with st.expander(f"📌 {day_label}", expanded=True):
                    if "schedule_style" in day_plan:
                        st.caption(f"Schedule style: {day_plan['schedule_style']}")
                    if "estimated_cost" in day_plan:
                        st.metric("Estimated Cost", f"${day_plan['estimated_cost']:,.0f}" if isinstance(day_plan['estimated_cost'], (int, float)) else str(day_plan['estimated_cost']))
                        if isinstance(day_plan['estimated_cost'], (int, float)):
                            cost_data.append({"Day": day_label, "Cost": day_plan['estimated_cost']})

                    if "attractions" in day_plan and isinstance(day_plan["attractions"], list):
                        st.markdown("**🎯 Attractions & Activities:**")
                        for attr in day_plan["attractions"]:
                            if isinstance(attr, dict):
                                attr_name = attr.get("name", attr.get("activity", ""))
                                details = [f"{k.replace('_',' ').title()}: {v}" for k, v in attr.items() if k not in ("name", "activity")]
                                st.markdown(f"  - **{attr_name}**" + (f" — {', '.join(details)}" if details else ""))
                            else:
                                st.markdown(f"  - {attr}")

                    if "travel_info" in day_plan:
                        ti = day_plan["travel_info"]
                        st.markdown("**🚗 Travel Info:**")
                        if isinstance(ti, dict):
                            for k, v in ti.items():
                                st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                        else:
                            st.markdown(f"  {ti}")

                    skip_keys = {"day", "title", "schedule_style", "estimated_cost", "attractions", "travel_info"}
                    for key, val in day_plan.items():
                        if key in skip_keys:
                            continue
                        if isinstance(val, list):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for item in val:
                                if isinstance(item, dict):
                                    parts = [f"{k.replace('_',' ').title()}: {v}" for k, v in item.items()]
                                    st.markdown(f"  - {', '.join(parts)}")
                                else:
                                    st.markdown(f"  - {item}")
                        elif isinstance(val, dict):
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            for k, v in val.items():
                                st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {val}")
            elif isinstance(day_plan, str):
                st.markdown(f"- {day_plan}")

        if cost_data:
            st.markdown("---")
            st.markdown("### 📊 Daily Cost Overview")
            df = pd.DataFrame(cost_data)
            fig = px.bar(df, x="Day", y="Cost", title="Estimated Daily Costs", text_auto=".0f")
            fig.update_layout(yaxis_title="Cost ($)")
            st.plotly_chart(fig, use_container_width=True)


def render_budget(data: dict):
    st.subheader("💰 Budget Analysis")

    total = data.get("total_budget", 0)
    days = data.get("days", 1)
    group_size = data.get("group_size", 1)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", f"${total:,.0f}")
    col2.metric("Trip Duration", f"{days} days")
    col3.metric("Travelers", f"{group_size}")

    category_breakdown = data.get("category_breakdown", [])
    daily_spending = data.get("daily_spending", [])

    if category_breakdown:
        st.markdown("### Category Allocation")

        categories = [item["category"] for item in category_breakdown]
        amounts = [item["amount"] for item in category_breakdown]
        percentages = [item["percentage"] for item in category_breakdown]

        col_pie, col_bar = st.columns(2)

        with col_pie:
            fig_pie = px.pie(
                names=categories,
                values=amounts,
                title="Budget Distribution",
                hole=0.3,
            )
            fig_pie.update_traces(textinfo="percent+label")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_bar:
            fig_bar = px.bar(
                x=categories,
                y=amounts,
                title="Budget by Category",
                labels={"x": "Category", "y": "Amount ($)"},
                text=[f"${a:,.0f} ({p:.0f}%)" for a, p in zip(amounts, percentages)],
            )
            fig_bar.update_traces(textposition="outside")
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    if daily_spending:
        st.markdown("### Daily Spending Breakdown")

        df = pd.DataFrame(daily_spending)

        spending_categories = ["accommodation", "meals", "transportation", "activities", "miscellaneous"]
        available_cols = [c for c in spending_categories if c in df.columns]

        if available_cols and "day" in df.columns:
            fig_line = go.Figure()
            for cat in available_cols:
                fig_line.add_trace(go.Scatter(
                    x=df["day"],
                    y=df[cat],
                    mode="lines+markers",
                    name=cat.title(),
                    stackgroup="one",
                ))
            fig_line.update_layout(
                title="Daily Spending by Category (Stacked)",
                xaxis_title="Day",
                yaxis_title="Amount ($)",
                hovermode="x unified",
            )
            st.plotly_chart(fig_line, use_container_width=True)

        if "total" in df.columns and "day" in df.columns:
            cumulative = df["total"].cumsum()
            fig_cumulative = go.Figure()
            fig_cumulative.add_trace(go.Scatter(
                x=df["day"],
                y=cumulative,
                mode="lines+markers",
                name="Cumulative Spending",
                fill="tozeroy",
            ))
            fig_cumulative.add_hline(
                y=total,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Budget Limit: ${total:,.0f}",
            )
            fig_cumulative.update_layout(
                title="Cumulative Spending vs Budget",
                xaxis_title="Day",
                yaxis_title="Total Spent ($)",
            )
            st.plotly_chart(fig_cumulative, use_container_width=True)

    if "advice" in data:
        st.info(f"**Budget Advice:** {data['advice']}")


def render_value(val, indent=0):
    prefix = "  " * indent
    if isinstance(val, list):
        for item in val:
            if isinstance(item, dict):
                parts = [f"{k.replace('_', ' ').title()}: {v}" for k, v in item.items()]
                st.markdown(f"{prefix}- {', '.join(parts)}")
            else:
                st.markdown(f"{prefix}- {item}")
    elif isinstance(val, dict):
        for k, v in val.items():
            if isinstance(v, (dict, list)):
                st.markdown(f"{prefix}**{k.replace('_', ' ').title()}:**")
                render_value(v, indent + 1)
            else:
                st.markdown(f"{prefix}- **{k.replace('_', ' ').title()}:** {v}")
    else:
        st.markdown(f"{prefix}{val}")


def render_full_plan(data: dict):
    st.subheader("📋 Complete Travel Plan")

    if "trip_summary" in data:
        st.markdown("### ✈️ Trip Summary")
        summary = data["trip_summary"]
        if isinstance(summary, dict):
            highlights = summary.get("highlights", [])
            main_info = {k: v for k, v in summary.items() if k != "highlights"}
            if main_info:
                cols = st.columns(min(len(main_info), 4))
                for i, (key, val) in enumerate(main_info.items()):
                    cols[i % len(cols)].metric(key.replace("_", " ").title(), str(val))
            if highlights:
                st.markdown("**Highlights:**")
                for h in highlights:
                    st.markdown(f"  - {h}")
        elif isinstance(summary, str):
            st.markdown(summary)

    if "daily_plan" in data:
        st.markdown("---")
        st.markdown("### 📅 Daily Schedule")
        daily = data["daily_plan"]
        if isinstance(daily, list):
            for day_plan in daily:
                if isinstance(day_plan, dict):
                    day_num = day_plan.get("day", day_plan.get("title", "Day"))
                    day_label = f"Day {day_num}" if isinstance(day_num, int) else str(day_num)
                    with st.expander(f"📌 {day_label}", expanded=True):
                        if "weather_summary" in day_plan:
                            st.caption(f"🌤️ {day_plan['weather_summary']}")

                        time_slots = ["morning", "afternoon", "evening"]
                        slot_cols = st.columns(3)
                        for idx, slot in enumerate(time_slots):
                            if slot in day_plan:
                                with slot_cols[idx]:
                                    st.markdown(f"**{slot.title()}**")
                                    slot_data = day_plan[slot]
                                    if isinstance(slot_data, dict):
                                        for k, v in slot_data.items():
                                            st.markdown(f"- {k.replace('_', ' ').title()}: {v}")
                                    else:
                                        st.markdown(str(slot_data))

                        if "meals" in day_plan:
                            st.markdown("**🍽️ Meals:**")
                            meals = day_plan["meals"]
                            if isinstance(meals, dict):
                                meal_cols = st.columns(3)
                                for idx, (meal, info) in enumerate(meals.items()):
                                    with meal_cols[idx % 3]:
                                        st.markdown(f"**{meal.title()}**")
                                        if isinstance(info, dict):
                                            for k, v in info.items():
                                                st.markdown(f"- {k.replace('_', ' ').title()}: {v}")
                                        else:
                                            st.markdown(str(info))

                        if "notes" in day_plan:
                            st.info(f"💡 {day_plan['notes']}")

                        skip_keys = {"day", "title", "weather_summary", "morning", "afternoon", "evening", "meals", "notes"}
                        for key, val in day_plan.items():
                            if key in skip_keys:
                                continue
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            render_value(val)
                elif isinstance(day_plan, str):
                    st.markdown(f"- {day_plan}")

    if "accommodation" in data:
        st.markdown("---")
        st.markdown("### 🏨 Accommodation")
        acc = data["accommodation"]
        if isinstance(acc, dict):
            name = acc.get("hotel_name", acc.get("name", ""))
            if name:
                st.markdown(f"**{name}**")
            col1, col2 = st.columns(2)
            for key, val in acc.items():
                if key in ("hotel_name", "name"):
                    continue
                if isinstance(val, (dict, list)):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    render_value(val)
                else:
                    col1.markdown(f"- **{key.replace('_', ' ').title()}:** {val}")
        elif isinstance(acc, str):
            st.markdown(acc)

    if "dining_plan" in data:
        st.markdown("---")
        st.markdown("### 🍽️ Dining Plan")
        dining = data["dining_plan"]
        if isinstance(dining, dict):
            for key, val in dining.items():
                if isinstance(val, list):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    for item in val:
                        if isinstance(item, dict):
                            parts = [f"{k.replace('_', ' ').title()}: {v}" for k, v in item.items()]
                            st.markdown(f"  - {', '.join(parts)}")
                        else:
                            st.markdown(f"  - {item}")
                elif isinstance(val, dict):
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    for k, v in val.items():
                        st.markdown(f"  - {k.replace('_', ' ').title()}: {v}")
                else:
                    st.markdown(f"- **{key.replace('_', ' ').title()}:** {val}")
        elif isinstance(dining, str):
            st.markdown(dining)

    if "budget_breakdown" in data:
        st.markdown("---")
        st.markdown("### 💰 Budget Breakdown")
        budget = data["budget_breakdown"]
        if isinstance(budget, dict):
            numeric_items = {k: v for k, v in budget.items() if isinstance(v, (int, float))}
            if numeric_items:
                fig = px.pie(
                    names=[k.replace("_", " ").title() for k in numeric_items.keys()],
                    values=list(numeric_items.values()),
                    title="Budget Allocation",
                    hole=0.3,
                )
                fig.update_traces(textinfo="percent+label+value")
                st.plotly_chart(fig, use_container_width=True)

                table_data = [{"Category": k.replace("_", " ").title(), "Amount": f"${v:,.0f}" if isinstance(v, (int, float)) else str(v)} for k, v in budget.items()]
                st.table(table_data)
            else:
                for key, val in budget.items():
                    st.markdown(f"- **{key.replace('_', ' ').title()}:** {val}")
        elif isinstance(budget, str):
            st.markdown(budget)

    if "packing_tips" in data:
        st.markdown("---")
        st.markdown("### 🎒 Packing Tips")
        tips = data["packing_tips"]
        if isinstance(tips, list):
            cols = st.columns(2)
            half = len(tips) // 2 + 1
            for i, tip in enumerate(tips):
                cols[0 if i < half else 1].markdown(f"- {tip}")
        elif isinstance(tips, str):
            st.markdown(tips)

    if "safety_advice" in data:
        st.markdown("---")
        st.markdown("### ⚠️ Safety Advice")
        st.warning(data["safety_advice"])


def display_raw_data(data: dict):
    with st.expander("📄 View Raw JSON Response"):
        st.code(json.dumps(data, indent=2, default=str), language="json")


# --- MAIN UI ---
st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip with AI-powered agents that find weather, hotels, restaurants, attractions, and build your itinerary.")

st.divider()

# Sidebar for inputs
with st.sidebar:
    st.header("🗺️ Trip Parameters")

    planning_mode = st.selectbox(
        "Planning Mode",
        ["Full Travel Plan", "Budget Analysis", "Weather Only", "Hotels Only", "Restaurants Only", "Attractions Only", "Itinerary Only"],
    )

    st.divider()

    # Core parameters (always shown)
    st.subheader("📍 Destination")
    location = st.text_input("Location", placeholder="e.g., Bolinao, Pangasinan, Philippines")

    # Conditional parameters based on mode
    if planning_mode != "Weather Only":
        st.subheader("📆 Trip Details")
        days = st.slider("Number of Days", min_value=1, max_value=30, value=3)
        group_size = st.slider("Number of Travelers", min_value=1, max_value=50, value=2)

    if planning_mode in ["Full Travel Plan", "Budget Analysis", "Hotels Only", "Itinerary Only"]:
        st.subheader("💰 Budget")
        total_budget = st.text_input("Total Budget", placeholder="e.g., $1500 - $2000")

    if planning_mode in ["Full Travel Plan", "Budget Analysis", "Hotels Only"]:
        st.subheader("🏨 Hotel Preferences")
        hotel_preference = st.text_input("Hotel Preference", placeholder="e.g., beachfront resort, mid-range")

    if planning_mode in ["Full Travel Plan", "Budget Analysis", "Restaurants Only"]:
        st.subheader("🍽️ Dining Preferences")
        restaurant_preference = st.text_input("Cuisine Preference", placeholder="e.g., Filipino cuisine, seafood")
        dietary_restrictions = st.text_input("Dietary Restrictions", placeholder="e.g., None, vegetarian, halal")
        meal_budget_per_day = st.text_input("Meal Budget Per Day", placeholder="e.g., $50")

    if planning_mode in ["Full Travel Plan", "Budget Analysis", "Attractions Only", "Itinerary Only"]:
        st.subheader("🎯 Interests & Style")
        interests = st.text_input("Interests", placeholder="e.g., beaches, snorkeling, historical sites")
        intensity = st.selectbox("Activity Intensity", ["light", "moderate", "intense"])
        events = st.text_input("Events/Festivals", placeholder="e.g., local festivals, cultural events")

    if planning_mode in ["Full Travel Plan", "Budget Analysis", "Itinerary Only"]:
        st.subheader("📅 Schedule Style")
        schedule_style = st.selectbox("Schedule Style", ["balanced", "packed", "relaxed"])

    st.divider()
    generate_btn = st.button("🚀 Generate Plan", type="primary", use_container_width=True)


# Main content area
if generate_btn:
    if not location:
        st.error("Please enter a destination location.")
    else:
        result = None

        if planning_mode == "Weather Only":
            with st.spinner("🌤️ Checking weather forecast..."):
                result = call_api("/travel/forecast", {"location": location})
            if result:
                render_weather(result)

        elif planning_mode == "Hotels Only":
            if not total_budget or not hotel_preference:
                st.error("Please fill in all hotel-related fields.")
            else:
                with st.spinner("🏨 Finding hotels..."):
                    payload = {
                        "location": location,
                        "days": days,
                        "group_size": group_size,
                        "total_budget": total_budget,
                        "hotel_preference": hotel_preference,
                    }
                    result = call_api("/travel/hotels", payload)
                if result:
                    render_hotels(result)

        elif planning_mode == "Restaurants Only":
            if not restaurant_preference or not dietary_restrictions or not meal_budget_per_day:
                st.error("Please fill in all restaurant-related fields.")
            else:
                with st.spinner("🍽️ Finding restaurants..."):
                    payload = {
                        "location": location,
                        "days": days,
                        "group_size": group_size,
                        "restaurant_preference": restaurant_preference,
                        "dietary_restrictions": dietary_restrictions,
                        "meal_budget_per_day": meal_budget_per_day,
                    }
                    result = call_api("/travel/restaurants", payload)
                if result:
                    render_restaurants(result)

        elif planning_mode == "Attractions Only":
            if not interests or not events:
                st.error("Please fill in all attraction-related fields.")
            else:
                with st.spinner("🎯 Discovering attractions..."):
                    payload = {
                        "location": location,
                        "days": days,
                        "group_size": group_size,
                        "interests": interests,
                        "intensity": intensity,
                        "events": events,
                    }
                    result = call_api("/travel/attractions", payload)
                if result:
                    render_attractions(result)

        elif planning_mode == "Itinerary Only":
            if not total_budget or not interests or not events:
                st.error("Please fill in all itinerary-related fields.")
            else:
                with st.spinner("📅 Building itinerary..."):
                    payload = {
                        "location": location,
                        "days": days,
                        "group_size": group_size,
                        "total_budget": total_budget,
                        "interests": interests,
                        "intensity": intensity,
                        "events": events,
                        "schedule_style": schedule_style,
                    }
                    result = call_api("/travel/itenerary", payload)
                if result:
                    render_itinerary(result)

        elif planning_mode == "Budget Analysis":
            if not all([total_budget, hotel_preference, restaurant_preference,
                       dietary_restrictions, meal_budget_per_day, interests, events]):
                st.error("Please fill in all fields for budget analysis.")
            else:
                with st.spinner("💰 AI agents are analyzing your budget... This may take a few minutes."):
                    payload = {
                        "location": location,
                        "days": days,
                        "group_size": group_size,
                        "total_budget": total_budget,
                        "interests": interests,
                        "intensity": intensity,
                        "events": events,
                        "schedule_style": schedule_style,
                        "hotel_preference": hotel_preference,
                        "restaurant_preference": restaurant_preference,
                        "dietary_restrictions": dietary_restrictions,
                        "meal_budget_per_day": meal_budget_per_day,
                    }
                    result = call_api("/travel/budget", payload)
                if result:
                    render_budget(result)

        elif planning_mode == "Full Travel Plan":
            if not all([total_budget, hotel_preference, restaurant_preference,
                       dietary_restrictions, meal_budget_per_day, interests, events]):
                st.error("Please fill in all fields for a full travel plan.")
            else:
                with st.spinner("✈️ AI agents are building your complete travel plan... This may take a few minutes."):
                    payload = {
                        "location": location,
                        "days": days,
                        "group_size": group_size,
                        "total_budget": total_budget,
                        "restaurant_preference": restaurant_preference,
                        "dietary_restrictions": dietary_restrictions,
                        "meal_budget_per_day": meal_budget_per_day,
                        "hotel_preference": hotel_preference,
                        "interests": interests,
                        "intensity": intensity,
                        "events": events,
                        "schedule_style": schedule_style,
                    }
                    result = call_api("/travel/plan", payload)
                if result:
                    render_full_plan(result)

        # Show raw data and PDF download
        if result:
            display_raw_data(result)

            st.divider()
            st.subheader("📥 Download PDF Report")
            pdf_bytes = generate_travel_pdf(result, location, planning_mode)
            st.download_button(
                label="📄 Download Travel Plan as PDF",
                data=pdf_bytes,
                file_name=f"travel_plan_{location.replace(' ', '_').replace(',', '')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

else:
    st.markdown(
        """
        ### How to use:
        1. **Select a planning mode** from the sidebar
        2. **Fill in your trip parameters** (destination, dates, preferences)
        3. **Click "Generate Plan"** to let our AI agents work their magic
        4. **Download the PDF** of your complete travel plan

        ---

        ### Available AI Agents:
        | Agent | Purpose |
        |-------|---------|
        | 🌤️ Weather Forecaster | Current weather & 5-day forecast with travel advice |
        | 🏨 Hotel Finder | Top hotel recommendations based on budget & preferences |
        | 🍽️ Restaurant Finder | Restaurant picks considering cuisine & dietary needs |
        | 🎯 Attraction Guide | Top 10 attractions tailored to your interests |
        | 📅 Itinerary Organizer | Day-by-day optimized schedule |
        | 💰 Budget Analyst | Budget breakdown with pie charts, bar graphs & daily spending |
        | ✈️ Travel Planner | Master agent compiling everything into one plan |
        """
    )
