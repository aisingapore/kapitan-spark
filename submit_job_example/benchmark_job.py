
import base64
import io
import sys

import plotly.express as px
from pyspark.sql.types import StringType, StructField, StructType
from tpcds_pyspark import TPCDS

tpcds = TPCDS(data_path="/opt/spark/work-dir/tpcds_100")
tpcds.map_tables()
results = tpcds.run_TPCDS()
tpcds.print_test_results()
tpcds.aggregated_results_pdf
tpcds.grouped_results_pdf
tpcds.grouped_results_pdf.columns

fig = px.bar(tpcds.grouped_results_pdf.reset_index(), x='query', y=['executorRunTime', 'executorCpuTime'], 
             title='Executor Run Time and CPU Time per Query', barmode='group',
             labels={'value': 'Time (ms)', 'variable': 'Metric'}) # Customizing y-axis label and legend title)


fig.write_image("/opt/spark/work-dir/tpcds_output_100.png") 
