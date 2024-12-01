import {
	Button,
	FileInput,
	Label,
	Table,
	Textarea,
	TextInput,
} from "flowbite-react";
import React, { useState } from "react";
import * as XLSX from "xlsx";

const ExcelFiles = () => {
	const [files, setFiles] = useState(null);
	const [pattern, setPattern] = useState("");
	const [data, setData] = useState([]);

	const handleSearch = async (event) => {
		event.preventDefault();

		if (!files || files.length === 0 || !pattern) {
			console.log("Please upload files and enter a pattern to search.");
			return;
		}

		const lowerCasePattern = pattern.toLowerCase().trim(); // Convert the pattern to lowercase for case-insensitive search

		const fileReaders = Array.from(files).map((file) => {
			return new Promise((resolve, reject) => {
				if (
					file.type === "application/vnd.ms-excel" ||
					file.type ===
						"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
				) {
					const reader = new FileReader();
					reader.onload = (e) => {
						const binaryString = e.target.result;
						const workbook = XLSX.read(binaryString, { type: "binary" });

						const sheetNames = workbook.SheetNames;
						let matches = [];
						let headers = null; // To store the header row (if present)

						sheetNames.forEach((sheetName) => {
							const worksheet = workbook.Sheets[sheetName];
							const data = XLSX.utils.sheet_to_json(worksheet, { header: 1 }); // Get raw data as array of arrays

							if (data.length > 0 && !headers) {
								headers = data[0]; // Assume the first row as headers
							}

							// Search in each row for the pattern
							data.forEach((row, rowIndex) => {
								const rowMatch = row.some(
									(cell) =>
										cell &&
										cell.toString().toLowerCase().includes(lowerCasePattern)
								);
								if (rowMatch) {
									matches.push({
										sheetName,
										rowIndex: rowIndex + 1,
										rowData: row, // Store the entire row
									});
								}
							});
						});

						resolve({ fileName: file.name, headers, matches });
					};
					reader.onerror = (err) => reject(err);
					reader.readAsBinaryString(file);
				} else {
					resolve({ fileName: file.name, headers: null, matches: [] });
				}
			});
		});

		try {
			const results = await Promise.all(fileReaders);
			const searchResults = results.filter(
				(result) => result.matches.length > 0
			);

			setData((prevData) => [
				{
					pattern: pattern.trim(),
					files: Array.from(files).map((file) => file.name),
					searchResults,
				},
				...prevData,
			]);
		} catch (error) {
			console.error("Error reading files:", error);
		}
	};

	const handleDownload = (dataObject) => {};

	return (
		<div
			className="w-full bg-cover bg-center bg-fixed bg-no-repeat 
			bg-[url('../../light.jpg')] dark:bg-[url('../../dark.jpg')]">
			<div
				className="max-w-4xl my-10 mx-3 p-3 sm:mx-12 lg:mx-auto sm:p-10 self-center dark:shadow-whiteLg
			bg-transparent border-2 border-white/40 dark:border-white/20 backdrop-blur-[30px] rounded-lg shadow-xl bg-white bg-opacity-35 dark:bg-transparent dark:bg-opacity-100">
				<h1 className="text-center text-3xl mb-7 font-semibold uppercase">
					Data Searching in Excel Files
				</h1>
				<form className="flex flex-col gap-4" onSubmit={handleSearch}>
					<div>
						<Label value="Upload excel files" className="m-2" />
						<div className="flex gap-4">
							<FileInput
								type="file"
								accept=".xls, .xlsx"
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
						<Label value="Enter anything to search" className="m-2" />
						<Textarea
							type="text"
							placeholder="search???"
							rows={2}
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
						className="max-w-6xl my-10 mx-3 p-3 sm:mx-12 lg:mx-auto sm:p-10 self-center dark:shadow-whiteLg
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
							<div key={index} className="mt-5">
								<div
									className="overflow-x-scroll xl:overflow-visible p-4 md:max-w-md lg:max-w-6xl w-full mx-auto
										scrollbar scrollbar-track-slate-100 scrollbar-thumb-slate-300
										dark:scrollbar-track-slate-700 dark:scrollbar-thumb-slate-500 dark:shadow-whiteLg
										bg-transparent border-2 border-white/40 dark:border-white/20 rounded-lg shadow-xl">
									<h4 className="text-lg text-center mt-2 mb-5">
										Search Results in{" "}
										<span className="font-semibold">{result.fileName}</span>
									</h4>
									<Table
										hoverable
										className="backdrop-blur-[20px] bg-transparent border-2 border-white/20 
												rounded-lg shadow-lg dark:shadow-whiteLg">
										<Table.Head className="sticky top-[60px] z-10">
											<Table.HeadCell>Row Number</Table.HeadCell>
											{result.headers && // Display headers if present
												result.headers.map((header, index) => (
													<Table.HeadCell key={index}>{header}</Table.HeadCell>
												))}
										</Table.Head>
										<Table.Body>
											{result.matches.map((match, index) => (
												<Table.Row key={index}>
													<Table.Cell>{match.rowIndex}</Table.Cell>
													{match.rowData.map((cell, cellIndex) => {
														const cellContent = cell.toString();
														const highlightedContent = cellContent
															.split(
																new RegExp(`(${dataObject.pattern})`, "gi")
															)
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
															);
														return (
															<Table.Cell key={cellIndex}>
																{highlightedContent}
															</Table.Cell>
														);
													})}
												</Table.Row>
											))}
										</Table.Body>
									</Table>
								</div>
							</div>
						))}

						<div className="flex justify-between mt-10">
							<span>
								Click the "Download" button to save the above search results as
								a excel file.
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

export default ExcelFiles;
