# Based on https://github.com/ap3xx/link-airflow-plugins/blob/master/link.sh

PythonHome=".venv/lib/python3.6/site-packages/airflow"
PluginName=pipeline_plugin
PluginFolder="plugins"
NecessaryLinks="operators"

echo "Copy the following commands in your terminal to symlink the operators"

echo "ln -snf $PWD/$PluginFolder/$PluginName/operators $PWD/$PythonHome/operators/$PluginName"
echo "ln -snf $PWD/$PluginFolder/$PluginName $PWD/$PythonHome/$PluginName"
