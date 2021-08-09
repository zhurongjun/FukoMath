require ("vstudio")

work_space = "workspace/".._ACTION

-- windows 
PlatformMSVC64AVX2		= "MSVC 64 AVX2"
PlatformMSVC64AVX		= "MSVC 64 AVX"
PlatformMSVC64SSE41		= "MSVC 64 SSE 4.1"
PlatformMSVC64SSE2		= "MSVC 64 SSE 2"
PlatformMSVC64Scalar	= "MSVC 64 Scalar"
PlatformMSVC32SSE2		= "MSVC 32 SSE 2"
PlatformLLVM64AVX		= "LLVM 64 AVX"
PlatformLLVM64SSE41		= "LLVM 64 SSE 4.1"
PlatformLLVM64SSE2		= "LLVM 64 SSE 2"
PlatformLLVM32SSE2		= "LLVM 32 SSE 2"

-- osx 
PlatformOSX64			= "OSX 64"

-- linux 
PlatformLinux64_GCC		= "Linux64_GCC"
PlatformLinux64_Clang	= "Linux64_Clang"

-- NEON
PlatformARM 			= "MSVC ARM"
PlatformARM64 			= "MSVC ARM64"
PlatformAndroidARM 		= "Android ARM"
PlatformAndroidARM64 	= "Android ARM64"

-- platform 
isMacBuild = _ACTION == "xcode4"
isLinuxBuild = _ACTION == "gmake2"
isWindowsBuild = not isMacBuild and not isLinuxBuild
supportsARMBuild = _ACTION == "vs2017" or _ACTION == "vs2019"

-- paths 
fuko_math_lib_path = "FukoMath"

workspace("fuko_math")
    configurations { "Debug", "Release" }
	location (work_space)

	-- build flag 
    flags
	{
		"multiprocessorcompile", -- /MP
	}
	
	-- include dir 
    includedirs
	{
		fuko_math_lib_path,
	}

	-- cpp setttings 
    vectorextensions("sse4.1")
	cppdialect("c++17")

	-- per platform setup
	if(isMacBuild) then
		-- mac config 
		platforms { PlatformOSX64 }
		toolset("clang")
		architecture("x64")
		buildoptions { "-std=c++17 -msse4.1 -Wno-unused-variable" }
		linkoptions { "-stdlib=libc++" }
		
	elseif(isLinuxBuild) then
		-- linux config 
		platforms { PlatformLinux64_GCC, PlatformLinux64_Clang }
		architecture("x64")
		buildoptions { "-std=c++17 -msse4.1 -Wno-unused-variable" }
		
		filter { "platforms:"..PlatformLinux64_GCC }
			toolset("gcc")
		
		filter { "platforms:"..PlatformLinux64_Clang }
			toolset("clang")
		
	else
		-- window config 
		platforms
		{
			PlatformMSVC64AVX2,
			PlatformMSVC64AVX,
			PlatformMSVC64SSE41,
			PlatformMSVC64SSE2,
			PlatformMSVC64Scalar,
			PlatformMSVC32SSE2, 
			
			PlatformLLVM64AVX,
			PlatformLLVM64SSE41,
			PlatformLLVM64SSE2,
			PlatformLLVM32SSE2, 
		}

		if(supportsARMBuild) then

			platforms
			{
				PlatformARM, 
				PlatformARM64, 
				PlatformAndroidARM, 
				PlatformAndroidARM64
			}

		end
	
		local llvmToolset;
		
		if (_ACTION == "vs2015") then
			llvmToolset = "msc-llvm-vs2014";
		else
			llvmToolset = "msc-llvm";
		end
		
		--setup startup project 
		startproject("fuko_math")
		
		filter { "platforms:"..PlatformMSVC64AVX2 }
			toolset("msc")
			architecture("x64")
			vectorextensions("avx2")
		
		filter { "platforms:"..PlatformMSVC64AVX }
			toolset("msc")
			architecture("x64")
			vectorextensions("avx")
		
		filter { "platforms:"..PlatformMSVC64SSE41 }
			toolset("msc")
			architecture("x64")
			vectorextensions("sse4.1")
			defines { "__SSE4_1__" }
			
		filter { "platforms:"..PlatformMSVC64SSE2 }
			toolset("msc")
			architecture("x64")
			vectorextensions("sse2")
			
		filter { "platforms:"..PlatformMSVC64Scalar }
			toolset("msc")
			architecture("x64")
		
		filter { "platforms:"..PlatformMSVC32SSE2 }
			toolset("msc")
			vectorextensions("sse2")
			
		filter { "platforms:"..PlatformLLVM64AVX }
			toolset(llvmToolset)
			architecture("x64")
			vectorextensions("avx")
			buildoptions { "-Wno-unused-variable -mavx" }
			
		filter { "platforms:"..PlatformLLVM64SSE41 }
			toolset(llvmToolset)
			architecture("x64")
			vectorextensions("sse4.1")
			defines { "__SSE4_1__" }
			buildoptions { "-Wno-unused-variable -msse4.1" }
			
		filter { "platforms:"..PlatformLLVM64SSE2 }
			toolset(llvmToolset)
			architecture("x64")
			vectorextensions("sse2")
			
		filter { "platforms:"..PlatformLLVM32SSE2 }
			toolset(llvmToolset)
			buildoptions { "-Wno-unused-variable" }
			
		filter { "platforms:"..PlatformARM }
			architecture("arm")
			vectorextensions ("neon")
			
		filter { "platforms:"..PlatformARM64 }
			architecture("arm64")
			vectorextensions ("neon")
			
		filter { "platforms:"..PlatformAndroidARM }
			system("android")
			architecture("arm")
			vectorextensions("neon")
			buildoptions { "-Wno-unused-variable" }
			linkoptions { "-lm" } -- Link against the standard math library
			
		filter { "platforms:"..PlatformAndroidARM64 }
			system("android")
			architecture("arm64")
			vectorextensions("neon")
			buildoptions { "-Wno-unused-variable" }
			linkoptions { "-lm" } -- Link against the standard math library
			
		filter{}
	end

	configuration "Debug"
		defines { "DEBUG" }
		symbols "full"
		inlining("auto")
		optimize("debug")
	
	configuration "Release"
		defines { "NDEBUG" }
		optimize "on"
		inlining("auto")
		optimize("speed")

project ("fuko_math")
	kind("staticlib")
	language("c++")
	files
	{
		fuko_math_lib_path.."/**.h",
		-- TODO. natvis 
		-- fuko_math_lib_path.."/*.natvis"
	}