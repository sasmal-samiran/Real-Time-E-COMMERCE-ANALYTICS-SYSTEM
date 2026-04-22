from flask import Flask, render_template, request, jsonify
from datetime import datetime
from collections import defaultdict
import numpy as np

from cassandra.cluster import Cluster

from config import KEYSPACE, CASSANDRA_HOST

app = Flask(__name__)

try:
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect()
    session.set_keyspace(KEYSPACE)

except Exception as e:
        print(e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/funnel")
def funnel():
    return render_template("funnel.html")

@app.route("/segmentation")
def segmentation():
    return render_template("segmentation.html")

@app.route("/anomaly")
def anomaly():
    return render_template("anomaly.html")

@app.route("/insights")
def insights():
    return render_template("insights.html")


@app.route("/api/dashboard")
def dashboard_data():
    product_analysis_rows = session.execute("SELECT * FROM product_analysis")
    user_segments_rows = session.execute("SELECT * FROM user_segments")
    problem_products_rows = session.execute("SELECT * FROM problem_products")
    best_products_rows = session.execute("SELECT * FROM best_products")
    category_performance_rows = session.execute("SELECT * FROM category_performance")
    also_viewed_rows = session.execute("SELECT * FROM also_viewed")

    total_views = 0
    total_purchases = 0
    total_add_to_cart = 0
    revenue = 0

    product_stats = []
    time_series = defaultdict(int)
    user_trend = {
        "High Value": defaultdict(int),
        "Frequent Buyer": defaultdict(int),
        "Normal": defaultdict(int),
        "Inactive": defaultdict(int)
    }
    segment_count = {
        "High Value": 0,
        "Frequent Buyer": 0,
        "Normal": 0,
        "Inactive": 0
    }
    recommendations = defaultdict(list)

    # Aggregate problem products by category
    problem_categories = defaultdict(list)
    for row in problem_products_rows:
        if row.category in problem_categories:
            problem_categories[row.category] += row.purchases  # or views if needed
        else:
            problem_categories[row.category] = row.purchases

    # Aggregate best products by category
    best_categories = defaultdict(list)
    for row in best_products_rows:
        if row.category in best_categories:
            best_categories[row.category] += row.purchases
        else:
            best_categories[row.category] = row.purchases

    category_performance = {
        row.category: row.total_purchases
        for row in category_performance_rows
    }
    category_performance_sorted = dict(
        sorted(category_performance.items(), key=lambda x: x[1])
    )

    for row in user_segments_rows:
        if row.last_activity == None:
            break
        revenue += row.total_spent

        date = str(row.last_activity.date())
        segment = row.segment.strip()

        if segment in user_trend:
            user_trend[segment][date] += 1

        segment = row.segment.strip()
        if segment in segment_count:
            segment_count[segment] += 1

    user_trend = {k: dict(v) for k, v in user_trend.items()}

    for row in product_analysis_rows:
        total_views += row.views
        total_purchases += row.purchases
        total_add_to_cart += row.add_to_cart

        product_stats.append({
            "product_id": row.product_id,
            "views": row.views,
            "purchases": row.purchases
        })

        # group by date
        time_series[str(row.date)] += row.purchases

    # Top 5 products
    top_products = sorted(product_stats, key=lambda x: x["views"], reverse=True)[:10]
    top_purchased = sorted(product_stats, key=lambda x: x["purchases"], reverse=True)[:10]

    # ALSO VIEWED RECOMMENDATIONS

    for row in also_viewed_rows:
        recommendations[row.base_product].append((row.recommended_product, row.co_view_count))

    # Keep top 5 recommended products per base_product
    for base_product in recommendations:
        recommendations[base_product] = [p for p, _ in sorted(recommendations[base_product], key=lambda x: -x[1])[:5]]

    also_viewed_list = []
    for base_product, recs in recommendations.items():
        for rec in recs:
            also_viewed_list.append({
                "base_product": base_product,
                "recommended_product": rec
            })

    # ---- ANOMALY DETECTION ----
    # 1. Collect daily traffic and purchases
    daily_views = defaultdict(int)
    daily_purchases = defaultdict(int)

    for row in product_analysis_rows:
        day = str(row.date)
        daily_views[day] += row.views
        daily_purchases[day] += row.purchases

    def detect_anomalies(data_dict):
        values = np.array(list(data_dict.values()))
        mean = values.mean()
        std = values.std() if values.std() > 0 else 1
        anomalies = []
        for day, value in data_dict.items():
            z_score = (value - mean) / std
            if abs(z_score) > 2:  # threshold for anomaly
                anomalies.append({"date": day, "value": int(value), "z_score": round(z_score,2)})
        return anomalies
    
    traffic_anomalies = detect_anomalies(daily_views)
    purchase_anomalies = detect_anomalies(daily_purchases)

    # 3. Unusual user behavior (example: sudden inactivity in high-value users)
    unusual_users = []
    for row in user_segments_rows:
        if row.segment.strip() == "High Value":
            # e.g., last activity more than 7 days
            if (datetime.now().date() - row.last_activity.date()).days > 7:
                unusual_users.append({"user_id": row.user_id, "last_activity": str(row.last_activity.date())})


    return jsonify({
        "kpi": {
            "views": total_views,
            "purchases": total_purchases,
            "revenue": revenue,
            "purchase_rate": round(total_purchases / total_views, 2)
        },
        "top_products": top_products,
        "time_series": time_series,
        "top_purchased": top_purchased,
        "user_trend": user_trend,
        "user_segments": segment_count,
        "funnel": {
            "views": total_views,
            "add_to_cart": total_add_to_cart,
            "purchases": total_purchases
        },
        "problem_categories": problem_categories,
        "best_categories": best_categories,
        "categories": category_performance_sorted,
        "also_viewed": also_viewed_list,
        "anomalies": {
            "traffic_spikes": traffic_anomalies,
            "purchase_drops": purchase_anomalies,
            "unusual_users": unusual_users
        }
    })

if __name__ == "__main__":
    app.run(debug=True)