using NUnit.Framework;

// Instructs NUnit to execute test fixtures concurrently across available CPU cores
[assembly: Parallelizable(ParallelScope.Fixtures)]

// Sets the maximum number of worker threads. 
// Level 4 is ideal for balanced performance on local machines and standard CI runners
[assembly: LevelOfParallelism(4)]