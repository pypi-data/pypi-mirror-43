@rem Install the chocolatey packages we need
choco install -y git --params "'/GitOnlyOnPath /NoAutoCrlf /WindowsTerminal /NoShellIntegration /NoCredentialManager'" || goto :error
choco install -y curl python vcredist-all || goto :error

@rem Reload our environment variables from the registry so the `git` command works
call refreshenv
@echo on

@rem Forcibly disable the git credential manager
git config --system credential.helper "" || goto :error

@rem Install the Visual Studio 2017 Build Tools workloads and components we need, excluding components with known issues in containers
curl --progress -L "https://aka.ms/vs/15/release/vs_buildtools.exe" --output %TEMP%\vs_buildtools.exe || goto :error
%TEMP%\vs_buildtools.exe --quiet --wait --norestart --nocache ^
	--installPath C:\BuildTools ^
	--add Microsoft.VisualStudio.Workload.VCTools;includeRecommended ^
	--add Microsoft.VisualStudio.Workload.ManagedDesktopBuildTools;includeRecommended ^
	--add Microsoft.VisualStudio.Workload.UniversalBuildTools ^
	--add Microsoft.VisualStudio.Workload.NetCoreBuildTools ^
	--add Microsoft.VisualStudio.Workload.MSBuildTools ^
	--add Microsoft.VisualStudio.Component.NuGet
python C:\buildtools-exitcode.py %ERRORLEVEL% || goto :error

@rem Copy pdbcopy.exe to the expected location(s)
python C:\copy-pdbcopy.py || goto :error

@rem Clean up any temp files generated during prerequisite installation
rmdir /S /Q \\?\%TEMP%
mkdir %TEMP%

@rem Display a human-readable completion message
@echo off
@echo Finished installing build prerequisites and cleaning up temporary files.
goto :EOF

@rem If any of our essential commands fail, propagate the error code
:error
@echo off
exit /b %ERRORLEVEL%
