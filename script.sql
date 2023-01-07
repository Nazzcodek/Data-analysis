-- agg_public_holiday table script
CREATE TABLE nasibell8682_analytics.agg_public_holiday (
  ingestion_date DATE PRIMARY KEY,
  tt_order_hol_jan INT,
  tt_order_hol_feb INT,
  tt_order_hol_mar INT,
  tt_order_hol_apr INT,
  tt_order_hol_may INT,
  tt_order_hol_jun INT,
  tt_order_hol_jul INT,
  tt_order_hol_aug INT,
  tt_order_hol_sep INT,
  tt_order_hol_oct INT,
  tt_order_hol_nov INT,
  tt_order_hol_dec INT
);

INSERT INTO nasibell8682_analytics.agg_public_holiday (ingestion_date, tt_order_hol_jan, tt_order_hol_feb, tt_order_hol_mar, tt_order_hol_apr, tt_order_hol_may, tt_order_hol_jun, tt_order_hol_jul, tt_order_hol_aug, tt_order_hol_sep, tt_order_hol_oct, tt_order_hol_nov, tt_order_hol_dec)
SELECT CURRENT_DATE as ingestion_date,
       SUM(CASE WHEN month_name = 'January' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_jan,
       SUM(CASE WHEN month_name = 'February' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_feb,
       SUM(CASE WHEN month_name = 'March' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_mar,
       SUM(CASE WHEN month_name = 'April' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_apr,
       SUM(CASE WHEN month_name = 'May' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_may,
       SUM(CASE WHEN month_name = 'June' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_jun,
       SUM(CASE WHEN month_name = 'July' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_jul,
       SUM(CASE WHEN month_name = 'August' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_aug,
       SUM(CASE WHEN month_name = 'September' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_sep,
       SUM(CASE WHEN month_name = 'October' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_oct,
       SUM(CASE WHEN month_name = 'November' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_nov,
       SUM(CASE WHEN month_name = 'December' THEN tt_orders_hol ELSE 0 END) as tt_order_hol_dec
FROM (
  SELECT COUNT(*) as tt_orders_hol, TO_CHAR(o.order_date, 'Month') as month_name
  FROM nasibell8682_staging.orders o
  JOIN if_common.dim_dates d ON o.order_date = d.calendar_dt
  WHERE d.working_day = false AND d.day_of_the_week_num BETWEEN 1 AND 5
  GROUP BY TO_CHAR(o.order_date, 'Month')
) subquery;

-- agg_shipment script
CREATE TABLE nasibell8682_analytics.agg_shipments (
  ingestion_date DATE PRIMARY KEY,
  tt_late_shipments INT,
  tt_undelivered_items INT
);

INSERT INTO nasibell8682_analytics.agg_shipments (ingestion_date, tt_late_shipments, tt_undelivered_items)
SELECT CURRENT_DATE as ingestion_date,
       COALESCE((SELECT COUNT(*)
                 FROM nasibell8682_staging.shipments_deliveries s
                 JOIN nasibell8682_staging.orders o ON s.order_id = o.order_id
                 WHERE s.delivery_date IS NULL AND s.shipment_date >= o.order_date + INTERVAL '6' DAY), 0) as tt_late_shipments,
       COALESCE((SELECT COUNT(*)
                 FROM nasibell8682_staging.shipments_deliveries s
                 JOIN nasibell8682_staging.orders o ON s.order_id = o.order_id
                 WHERE s.delivery_date IS NULL AND s.shipment_date IS NULL AND date '2022-09-05' >= o.order_date + INTERVAL '15' DAY), 0) as tt_undelivered_items;

       -- create the best_performing_product table 
       CREATE TABLE nasibell8682_analytics.best_performing_product (
  ingestion_date DATE PRIMARY KEY NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  most_ordered_day DATE NOT NULL,
  is_public_holiday BOOLEAN NOT NULL,
  tt_review_points INTEGER NOT NULL,
  pct_one_star_review FLOAT NOT NULL,
  pct_two_star_review FLOAT NOT NULL,
  pct_three_star_review FLOAT NOT NULL,
  pct_four_star_review FLOAT NOT NULL,
  pct_five_star_review FLOAT NOT NULL,
  pct_early_shipments FLOAT NOT NULL,
  pct_late_shipments FLOAT NOT NULL
);
