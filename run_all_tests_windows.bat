@echo off
setlocal

REM Run from repository root
cd /d "%~dp0"

REM Ensure local package imports work
set PYTHONPATH=%CD%

REM Create output directories
if not exist data mkdir data
if not exist figures mkdir figures
if not exist logs mkdir logs

echo Running critical regime tests...
python experiments\critical_regime_tests.py > logs\critical_regime_tests.log 2>&1
if errorlevel 1 (
  echo critical_regime_tests failed. See logs\critical_regime_tests.log
  exit /b 1
)

echo Running spatial feedback tests...
python experiments\spatial_feedback_tests.py > logs\spatial_feedback_tests.log 2>&1
if errorlevel 1 (
  echo spatial_feedback_tests failed. See logs\spatial_feedback_tests.log
  exit /b 1
)

echo Running validation summary...
python validate_critical_tests.py > logs\validate_critical_tests.log 2>&1
if errorlevel 1 (
  echo validate_critical_tests failed. See logs\validate_critical_tests.log
  exit /b 1
)

echo All tests completed successfully.
echo Outputs saved to data\ and figures\
echo Logs saved to logs\

endlocal
