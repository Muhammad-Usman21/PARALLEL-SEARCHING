import {
	Button,
	FileInput,
	Label,
	Table,
	Textarea,
	TextInput,
} from "flowbite-react";
import React, { useState } from "react";

// import { jsPDF } from "jspdf"; // Import jsPDF if you're using a module system

// import * as pdfjsLib from "pdfjs-dist";
// pdfjsLib.GlobalWorkerOptions.workerSrc =
// 	"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js";

const ResearchFiles = () => {
	const [files, setFiles] = useState(null);
	const [pattern, setPattern] = useState("");
	const [data, setData] = useState([]);

	const handleSearch = async (event) => {
		event.preventDefault();

		if (files.length === 0 || !pattern) {
			console.log("Please upload files and enter a pattern to search.");
			return;
		}

		try {
			const formData = new FormData();
			formData.append("heading", pattern.toLowerCase().trim()); // Append the search pattern

			// Append each file to the FormData
			Array.from(files).forEach((file) => {
				formData.append("files", file);
			});

			// Send the request to the server with the files and the search pattern
			const response = await fetch("http://127.0.0.1:5000/researchFileSearch", {
				method: "POST",
				body: formData, // Send form data
			});

			if (!response.ok) {
				throw new Error(`Error: ${response.statusText}`);
			}

			// Receive the search results from the server
			const searchResults = await response.json();

			console.log(searchResults);
			searchResults.forEach((result) => {
				console.log(result.fileName);
				console.log(result.title);
				console.log(result.heading);
				console.log(result.paragraph);
			});

			// Optionally update the UI with the search results
			setData((prevData) => [
				{
					pattern: pattern.trim(),
					files: Array.from(files).map((file) => file.name),
					searchResults,
				},
				...prevData,
			]);
		} catch (error) {
			console.error("Error processing PDF files:", error);
		}
	};

	const handleDownload = async (dataObject) => {
		try {
			const response = await fetch("http://127.0.0.1:5000/generate-pdf", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(dataObject),
			});

			if (!response.ok) {
				throw new Error("Failed to generate PDF");
			}

			// Download the PDF
			const blob = await response.blob();
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement("a");
			a.href = url;
			a.download = `${dataObject.pattern}-${dataObject.files.length}files.pdf`;
			document.body.appendChild(a);
			a.click();
			a.remove();
			window.URL.revokeObjectURL(url);
		} catch (error) {
			console.error("Error:", error);
		}
	};

	return (
		<div
			className="w-full bg-cover bg-center bg-fixed bg-no-repeat 
			bg-[url('../../light.jpg')] dark:bg-[url('../../dark.jpg')]">
			<div
				className="max-w-4xl my-10 mx-3 p-3 sm:mx-12 lg:mx-auto sm:p-10 self-center dark:shadow-whiteLg
			bg-transparent border-2 border-white/40 dark:border-white/20 backdrop-blur-[30px] rounded-lg shadow-xl bg-white bg-opacity-35 dark:bg-transparent dark:bg-opacity-100">
				<h1 className="text-center text-3xl mb-7 font-semibold uppercase">
					Select Headings from Research Papers
				</h1>
				<form className="flex flex-col gap-4" onSubmit={handleSearch}>
					<div>
						<Label value="Upload PDF files" className="m-2" />
						<div className="flex gap-4">
							<FileInput
								type="file"
								accept=".pdf"
								required
								multiple
								onChange={(e) => setFiles(e.target.files)}
								className="w-full sm:w-auto flex-auto"
							/>
							{/* <Button
								type="button"
								gradientDuoTone="purpleToBlue"
								size="sm"
								className="focus:ring-1 w-full sm:w-28">
								Upload Files
							</Button> */}
						</div>
					</div>
					<div className="">
						<Label value="Enter the heading" className="m-2" />
						<Textarea
							type="text"
							placeholder="heading???"
							rows={1}
							value={pattern}
							required
							id="pattern"
							className="flex-1"
							onChange={(e) => setPattern(e.target.value)}
						/>
					</div>
					<Button
						type="submit"
						gradientDuoTone="purpleToPink"
						outline
						className="focus:ring-1 uppercase">
						Search
					</Button>
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
						{console.log(data)}

						{dataObject.searchResults.map((result, index) => (
							<div key={index} className="my-10">
								<hr className="my-5 border-gray-500" />
								<h4 className="text-lg font-semibold">{result.fileName}</h4>
								<h2 className="text-2xl font-semibold text-center my-2">
									{result.title}
								</h2>
								<p className="first-letter-uppercase text-lg font-semibold">
									{result.heading}
								</p>
								<p className="text-justify">{result.paragraph}</p>
							</div>
						))}

						<hr className="border-gray-500" />

						<div className="flex justify-between mt-10">
							<span>
								Click the "Download" button to save the above results as a pdf
								file.
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

export default ResearchFiles;
