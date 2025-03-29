"use client";

import type React from "react";

import { useState } from "react";
import { motion } from "framer-motion";
import { Download, Search, FileText, GraduationCap } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export default function ResearchFiles() {
	const [files, setFiles] = useState<FileList | null>(null);
	const [pattern, setPattern] = useState("");
	const [data, setData] = useState<any[]>([]);
	const [loading, setLoading] = useState(false);

	const handleSearch = async (event: React.FormEvent) => {
		event.preventDefault();
		setLoading(true);

		if (files?.length === 0 || !pattern) {
			console.log("Please upload files and enter a pattern to search.");
			setLoading(false);
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
			const response = await fetch(
				`${import.meta.env.VITE_APP_BACKEND_HOST}/researchFileSearch`,
				{
					method: "POST",
					body: formData, // Send form data
				}
			);

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

			setLoading(false);
		} catch (error) {
			setLoading(false);
			console.error("Error processing PDF files:", error);
		}
	};

	const handleDownload = (dataObject: any) => {
		console.log("Download functionality to be implemented");
	};

	const containerVariants = {
		hidden: { opacity: 0 },
		visible: {
			opacity: 1,
			transition: {
				staggerChildren: 0.1,
			},
		},
	};

	const itemVariants = {
		hidden: { y: 20, opacity: 0 },
		visible: {
			y: 0,
			opacity: 1,
			transition: { type: "spring", stiffness: 300, damping: 24 },
		},
	};

	return (
		<motion.div
			className="container py-12 px-4 md:px-8 mx-auto"
			variants={containerVariants}
			initial="hidden"
			animate="visible"
			layout
			transition={{ type: "spring", stiffness: 300, damping: 30 }}>
			{/* Main search panel with diagonal split design */}
			<motion.div
				variants={itemVariants}
				layout
				className="relative overflow-hidden rounded-[2rem] shadow-2xl mb-16">
				<div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-primary/5 to-transparent z-0" />
				<div className="absolute -top-24 -right-24 w-64 h-64 bg-primary/10 rounded-full blur-3xl opacity-70" />
				<div className="absolute -bottom-32 -left-32 w-96 h-96 bg-primary/10 rounded-full blur-3xl opacity-50" />

				<div className="relative z-10 grid md:grid-cols-2 gap-0">
					{/* Left side - Title and description */}
					<div className="p-8 md:p-12 flex flex-col justify-center">
						<motion.div
							initial={{ opacity: 0, y: 20 }}
							animate={{ opacity: 1, y: 0 }}
							transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
							layout>
							<h2 className="text-3xl md:text-4xl font-bold mb-4 tracking-tight">
								<span className="bg-clip-text text-transparent bg-gradient-to-r from-primary via-primary/80 to-primary/60">
									Research Papers
								</span>
							</h2>
							<p className="text-muted-foreground text-lg mb-6 md:pr-12">
								Upload your research papers and discover specific headings and
								sections with our advanced search tool.
							</p>

							{data.length > 0 && (
								<div className="flex items-center mt-4 text-sm text-primary/70">
									<span className="inline-block w-2 h-2 rounded-full bg-primary mr-2"></span>
									<span>
										{data.length} search{data.length !== 1 ? "es" : ""}{" "}
										performed
									</span>
								</div>
							)}
						</motion.div>
					</div>

					{/* Right side - Form */}
					<div className="bg-background/50 backdrop-blur-md p-8 md:p-12 rounded-l-[2rem] md:rounded-l-none rounded-b-[2rem]">
						<form className="space-y-8" onSubmit={handleSearch}>
							<motion.div
								initial={{ opacity: 0, y: 20 }}
								animate={{ opacity: 1, y: 0 }}
								transition={{ delay: 0.2, duration: 0.5 }}
								layout>
								<Label
									htmlFor="pattern"
									className="text-sm uppercase tracking-wider font-medium text-primary/70 mb-2 block">
									Search Heading
								</Label>
								<Textarea
									id="pattern"
									placeholder="What heading are you looking for in the research papers?"
									value={pattern}
									onChange={(e) => setPattern(e.target.value)}
									disabled={loading}
									required
									className="min-h-[120px] text-base bg-background/50 border-primary/20 focus:border-primary/40 rounded-xl resize-none shadow-inner"
								/>
							</motion.div>

							<motion.div
								initial={{ opacity: 0, y: 20 }}
								animate={{ opacity: 1, y: 0 }}
								transition={{ delay: 0.3, duration: 0.5 }}
								className="space-y-2"
								layout>
								<Label
									htmlFor="files"
									className="text-sm uppercase tracking-wider font-medium text-primary/70 mb-2 block">
									Upload Research Papers
								</Label>
								<div className="relative group">
									<div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-primary/5 rounded-xl blur opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
									<div className="relative border-2 border-dashed border-primary/30 rounded-xl p-8 text-center hover:border-primary/50 transition-colors duration-300">
										<Input
											id="files"
											type="file"
											accept=".pdf"
											multiple
											onChange={(e) => setFiles(e.target.files)}
											disabled={loading}
											required
											className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
										/>
										<div className="flex flex-col items-center justify-center gap-2 pointer-events-none">
											<div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
												<GraduationCap className="h-5 w-5 text-primary" />
											</div>
											<p className="text-sm font-medium">
												Drag research papers here or click to browse
											</p>
											<p className="text-xs text-muted-foreground">
												Supports PDF format
											</p>
											{files && files.length > 0 && (
												<div className="mt-2 text-primary text-sm font-medium">
													{files.length} file{files.length !== 1 ? "s" : ""}{" "}
													selected
												</div>
											)}
										</div>
									</div>
								</div>
							</motion.div>

							<motion.div
								initial={{ opacity: 0, y: 20 }}
								animate={{ opacity: 1, y: 0 }}
								transition={{ delay: 0.4, duration: 0.5 }}
								className="pt-4"
								layout>
								<Button
									type="submit"
									disabled={loading}
									className="w-full h-14 rounded-xl bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-primary-foreground shadow-lg hover:shadow-xl transition-all duration-300">
									{loading ? (
										<motion.div
											className="flex items-center justify-center gap-2"
											initial={{ opacity: 0 }}
											animate={{ opacity: 1 }}>
											<motion.div
												animate={{ rotate: 360 }}
												transition={{
													duration: 1,
													repeat: Number.POSITIVE_INFINITY,
													ease: "linear",
												}}
												className="w-5 h-5 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full"
											/>
											<span>Processing...</span>
										</motion.div>
									) : (
										<motion.div
											className="flex items-center justify-center gap-2"
											whileHover={{ scale: 1.03 }}
											whileTap={{ scale: 0.98 }}>
											<Search className="h-5 w-5" />
											<span className="font-medium">Search Papers</span>
										</motion.div>
									)}
								</Button>
							</motion.div>
						</form>
					</div>
				</div>
			</motion.div>

			{/* Results section */}
			{data.length > 0 && (
				<motion.div
					initial={{ opacity: 0 }}
					animate={{ opacity: 1 }}
					transition={{ duration: 0.5 }}
					className="space-y-12"
					layout>
					<div className="flex items-center justify-between">
						<h3 className="text-2xl font-bold text-primary/80">
							Search Results
						</h3>
						<div className="h-px flex-1 bg-gradient-to-r from-transparent via-primary/20 to-transparent mx-4"></div>
						<span className="text-sm text-muted-foreground">
							{data.length} searches
						</span>
					</div>

					{data.map((dataObject, index) => (
						<motion.div
							key={index}
							initial={{ opacity: 0, y: 30 }}
							animate={{ opacity: 1, y: 0 }}
							transition={{ delay: 0.1 * index, duration: 0.5 }}
							className="group"
							layout>
							<div className="bg-gradient-to-br from-primary/5 to-transparent p-1 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300">
								<div className="bg-card/80 backdrop-blur-md rounded-2xl overflow-hidden">
									{/* Result header */}
									<div className="p-6 md:p-8 border-b border-primary/10">
										<div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
											<div>
												<h4 className="text-xl font-semibold mb-1 group-hover:text-primary transition-colors duration-300">
													"{dataObject.pattern}"
												</h4>
												<p className="text-sm text-muted-foreground">
													From {dataObject.files.length} file
													{dataObject.files.length !== 1 ? "s" : ""}:{" "}
													{dataObject.files.join(", ")}
												</p>
											</div>
											<motion.div
												whileHover={{ scale: 1.05 }}
												whileTap={{ scale: 0.95 }}>
												<Button
													variant="outline"
													size="sm"
													onClick={() => handleDownload(dataObject)}
													className="rounded-full px-4 border-primary/20 hover:border-primary/40 hover:bg-primary/5 transition-all duration-300">
													<Download className="h-4 w-4 mr-2" />
													Download Results
												</Button>
											</motion.div>
										</div>
									</div>

									{/* Result content */}
									<div className="divide-y divide-primary/5">
										{dataObject.searchResults.map(
											(result: any, resultIndex: number) => (
												<motion.div
													key={resultIndex}
													initial={{ opacity: 0 }}
													animate={{ opacity: 1 }}
													transition={{
														delay: 0.1 * resultIndex,
														duration: 0.5,
													}}
													className="p-6 md:p-8 hover:bg-primary/5 transition-colors duration-300"
													layout>
													<div className="space-y-4">
														<div className="flex items-center gap-2 mb-4">
															<div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
																<FileText className="h-4 w-4 text-primary" />
															</div>
															<h5 className="font-medium">{result.fileName}</h5>
														</div>

														<div className="space-y-4 p-4 rounded-xl bg-background/80 border border-primary/10">
															<h2 className="text-xl font-semibold text-center bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
																{result.title}
															</h2>
															<div className="border-l-2 border-primary pl-4 py-2 bg-primary/5 rounded-r-lg">
																<p className="font-medium text-primary">
																	{result.heading}
																</p>
															</div>
															<div className="bg-background/50 p-4 rounded-lg border border-primary/10">
																<p className="text-sm text-justify leading-relaxed">
																	{result.paragraph}
																</p>
															</div>
														</div>
													</div>
												</motion.div>
											)
										)}
									</div>
								</div>
							</div>
						</motion.div>
					))}
				</motion.div>
			)}
		</motion.div>
	);
}
