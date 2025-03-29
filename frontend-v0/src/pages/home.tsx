"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useLocation, useNavigate } from "react-router-dom";

import TextFiles from "@/components/text-files";
import ExcelFiles from "@/components/excel-files";
import ResearchFiles from "@/components/research-files";
import { Sidebar } from "@/components/sidebar";
import { Header } from "@/components/header";
import { useMediaQuery } from "@/hooks/use-mobile";
import NotFound from "@/pages/not-found";

export default function Home() {
	const [tab, setTab] = useState("text");
	const [isMobileOpen, setIsMobileOpen] = useState(false);
	const [isCollapsed, setIsCollapsed] = useState(false);
	const isMobile = useMediaQuery("(max-width: 768px)");
	const location = useLocation();
	const navigate = useNavigate();

	useEffect(() => {
		// Get tab from URL query parameter
		const searchParams = new URLSearchParams(location.search);
		const tabFromUrl = searchParams.get("tab");

		if (tabFromUrl) {
			setTab(tabFromUrl);
		} else {
			// Redirect to /?tab=text if no tab is specified
			navigate("/?tab=text", { replace: true });
		}
	}, [location.search, navigate]);

	useEffect(() => {
		if (isMobile) {
			setIsCollapsed(true);
		}
	}, [isMobile]);

	const toggleMobileSidebar = () => {
		setIsMobileOpen(!isMobileOpen);
	};

	const toggleSidebar = () => {
		setIsCollapsed(!isCollapsed);
	};

	const handleTabChange = (newTab: string) => {
		setTab(newTab);

		// Update URL using React Router
		navigate(`/?tab=${newTab}`, { replace: false });

		if (isMobile) {
			setIsMobileOpen(false);
		}
	};

	const pageVariants = {
		initial: { opacity: 0, y: 10 },
		animate: { opacity: 1, y: 0 },
		exit: { opacity: 0, y: -10 },
	};

	return (
		<div className="min-h-screen bg-background text-foreground">
			<Header toggleSidebar={toggleMobileSidebar} isMobileOpen={isMobileOpen} />
			<Sidebar
				isMobileOpen={isMobileOpen}
				setIsMobileOpen={setIsMobileOpen}
				activeTab={tab}
				onTabChange={handleTabChange}
				isCollapsed={isCollapsed}
				toggleSidebar={toggleSidebar}
			/>
			<motion.main
				className="transition-all duration-300"
				initial={false}
				animate={{
					marginLeft: isMobile ? 0 : isCollapsed ? "80px" : "260px",
				}}
				transition={{
					type: "spring",
					stiffness: 300,
					damping: 30,
				}}>
				<AnimatePresence mode="wait">
					<motion.div
						key={tab}
						initial="initial"
						animate="animate"
						exit="exit"
						variants={pageVariants}
						transition={{
							duration: 0.4,
							ease: [0.22, 1, 0.36, 1],
						}}
						className="w-full min-h-[calc(100vh-4rem)]">
						{/* {tab === "text" && <TextFiles />}
						{tab === "excel" && <ExcelFiles />}
						{tab === "research" && <ResearchFiles />} */}

						{tab === "text" ? (
							<TextFiles />
						) : tab === "excel" ? (
							<ExcelFiles />
						) : tab === "research" ? (
							<ResearchFiles />
						) : (
							<NotFound />
						)}
					</motion.div>
				</AnimatePresence>
			</motion.main>
		</div>
	);
}
