import { Button, FileInput, Label, Textarea, TextInput } from "flowbite-react";
import React, { useState } from "react";

const TextFiles = () => {
	const [files, setFiles] = useState(null);
	const [pattern, setPattern] = useState("");
	const [data, setData] = useState([]);
	const [loading, setLoading] = useState(false);

	const handleSearch = async (event) => {
		event.preventDefault();
		setLoading(true);

		if (files.length === 0 || !pattern) {
			setLoading(false);
			console.log("Please upload files and enter a pattern to search.");
			return;
		}

		try {
			const formData = new FormData();
			formData.append("pattern", pattern.toLowerCase().trim()); // Append the search pattern
			Array.from(files).forEach((file) => {
				formData.append("files", file); // Append each file
			});

			const response = await fetch(
				`${import.meta.env.VITE_APP_BACKEND_HOST}/textFileSearch`,
				{
					method: "POST",
					body: formData, // Send form data
				}
			);

			if (!response.ok) {
				throw new Error(`Error: ${response.statusText}`);
			}

			const searchResults = await response.json();
			console.log(searchResults);

			setData((prevData) => [
				{
					pattern: pattern.trim(),
					files: Array.from(files).map((file) => file.name),
					searchResults,
				},
				...prevData,
			]);

			setLoading(false);
		} catch (error) {
			setLoading(false);
			console.error("Error reading files:", error);
		}
	};

	const handleDownload = (dataObject) => {
		if (!dataObject || !dataObject.searchResults) {
			console.error("No search results available to download.");
			return;
		}

		const resultsText =
			`SEARCH RESULTS FOR "${dataObject.pattern.toUpperCase()}"\nFrom Files: ${dataObject.files.join(
				", "
			)}\n\n\n` +
			dataObject.searchResults
				.map((result) => {
					const fileNameHeader = `Results for: ${result.fileName}\n`;
					const matchesText = result.matches
						// .map((match) => `Line ${match.lineNumber}: ${match.line}`)
						.map((match) => `${match.line}`)
						.join("\n");

					return `${fileNameHeader}${matchesText}\n\n`;
				})
				.join("\n");

		const blob = new Blob([resultsText], { type: "text/plain" });

		const link = document.createElement("a");
		link.href = URL.createObjectURL(blob);
		link.download = `${dataObject.pattern}-${dataObject.files.length}files.txt`;
		link.click();
	};

	return (
		<div
			className="w-full bg-cover bg-center bg-fixed bg-no-repeat 
			bg-[url('../../light.jpg')] dark:bg-[url('../../dark.jpg')]">
			<div
				className="max-w-4xl my-10 mx-3 p-3 sm:mx-12 lg:mx-auto sm:p-10 self-center dark:shadow-whiteLg
			bg-transparent border-2 border-white/40 dark:border-white/20 backdrop-blur-[30px] rounded-lg shadow-xl bg-white bg-opacity-35 dark:bg-transparent dark:bg-opacity-100">
				<h1 className="text-center text-3xl mb-7 font-semibold uppercase">
					Pattern Searching in Text/Docx/PDF Files
				</h1>
				<form className="flex flex-col gap-4" onSubmit={handleSearch}>
					<div className="">
						<Label value="Enter a pattern to search" className="m-2" />
						<Textarea
							type="text"
							placeholder="Pattern to search???"
							rows={1}
							disabled={loading}
							value={pattern}
							required
							id="pattern"
							className="flex-1"
							onChange={(e) => setPattern(e.target.value)}
						/>
					</div>
					<div>
						<Label value="Upload text, docx or pdf files" className="m-2" />
						<div className="flex gap-4">
							<FileInput
								type="file"
								accept=".txt,.docx,.pdf"
								required
								disabled={loading}
								multiple
								onChange={(e) => setFiles(e.target.files)}
								className="w-full sm:w-auto flex-auto"
							/>
							<Button
								type="submit"
								gradientDuoTone="purpleToPink"
								outline
								disabled={loading}
								className="focus:ring-1 uppercase w-[250px]">
								{loading ? "Processing... Please wait!" : "Search"}
							</Button>
						</div>
					</div>
				</form>
			</div>
			{data.length > 0 &&
				data.map((dataObject, index) => (
					<div
						key={index}
						className="max-w-4xl my-10 mx-3 p-3 sm:mx-12 lg:mx-auto sm:p-10 self-center dark:shadow-whiteLg
			            bg-transparent border-2 border-white/40 dark:border-white/20 backdrop-blur-[30px] rounded-lg shadow-xl bg-white bg-opacity-35 dark:bg-transparent dark:bg-opacity-100">
						<div className="flex flex-col gap-3">
							<h3 className="text-2xl uppercase text-center">
								Search Results for{" "}
								<span className="font-semibold">{dataObject.pattern}</span>
							</h3>
							<h2 className="text-xl text-center">
								From Files:{" "}
								<span className="font-semibold">
									{dataObject.files.join(", ")}
								</span>
							</h2>
						</div>
						{dataObject.searchResults.map((result, index) => (
							<div key={index} className="my-6">
								<hr className="border-gray-500 my-4" />
								<h4 className="text-lg font-semibold">{result.fileName}</h4>
								<p>
									{result.matches.map((match, idx) => (
										<p key={idx} className="text-justify">
											{/* <br />
											Process ID <strong>{match.processId}</strong> found the
											Line number <strong>{match.lineNumber}</strong> in file{" "}
											<strong>{match.fileName}</strong>
											<br /> */}
											{match.line
												.split(new RegExp(`(${dataObject.pattern})`, "gi"))
												.map((part, i) =>
													part.toLowerCase() ===
													dataObject.pattern.toLowerCase() ? (
														<span
															key={i}
															className="bg-yellow-100 dark:bg-yellow-800">
															{part}
														</span>
													) : (
														part
													)
												)}
										</p>
									))}
								</p>
							</div>
						))}
						<hr className="border-gray-500" />
						<div className="flex justify-between mt-6">
							<span>
								Click the "Download" button to save the above search results as
								a text file.
							</span>
							<Button
								type="button"
								gradientDuoTone="purpleToBlue"
								size="sm"
								onClick={() => {
									handleDownload(dataObject);
								}}
								outline
								className="focus:ring-1 w-full sm:w-28">
								Download
							</Button>
						</div>
					</div>
				))}
		</div>
	);
};

export default TextFiles;
