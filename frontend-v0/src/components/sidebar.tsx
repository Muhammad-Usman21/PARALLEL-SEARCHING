"use client";
import { motion, AnimatePresence } from "framer-motion";
import {
	FileText,
	Table,
	GraduationCap,
	ChevronLeft,
	ChevronRight,
	Settings,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useMediaQuery } from "@/hooks/use-mobile";

export function Sidebar({
	isMobileOpen,
	setIsMobileOpen,
	activeTab,
	onTabChange,
	isCollapsed,
	toggleSidebar,
}: {
	isMobileOpen: boolean;
	setIsMobileOpen: (open: boolean) => void;
	activeTab: string;
	onTabChange: (tab: string) => void;
	isCollapsed: boolean;
	toggleSidebar: () => void;
}) {
	const isMobile = useMediaQuery("(max-width: 768px)");

	const sidebarVariants = {
		expanded: { width: "260px" },
		collapsed: { width: "80px" },
	};

	// Mobile sidebar variants
	const mobileSidebarVariants = {
		open: {
			x: 0,
			opacity: 1,
			transition: {
				type: "spring",
				stiffness: 300,
				damping: 30,
			},
		},
		closed: {
			x: "-100%",
			opacity: 0,
			transition: {
				type: "spring",
				stiffness: 300,
				damping: 30,
			},
		},
	};

	const menuItems = [
		{
			id: "text",
			label: "Pattern Searching",
			icon: FileText,
			path: "/?tab=text",
		},
		{ id: "excel", label: "Excel Files", icon: Table, path: "/?tab=excel" },
		{
			id: "research",
			label: "Research Papers",
			icon: GraduationCap,
			path: "/?tab=research",
		},
	];

	const handleTabChange = (newTab: string) => {
		onTabChange(newTab);
	};

	// Desktop sidebar
	const DesktopSidebar = () => (
		<motion.div
			className={cn(
				"h-[calc(100vh-4rem)] fixed top-16 left-0 z-20 pt-6 pb-6 flex flex-col",
				"bg-background/95 backdrop-blur-md border-r border-border/50"
			)}
			variants={sidebarVariants}
			initial={false}
			animate={isCollapsed ? "collapsed" : "expanded"}
			transition={{ duration: 0.4, ease: [0.25, 1, 0.5, 1] }}>
			<div className="flex-1 overflow-y-auto px-3 py-10 space-y-6">
				<div className="space-y-1.5">
					{menuItems.map((item) => (
						<motion.div
							key={item.id}
							whileHover={{ x: 4 }}
							whileTap={{ scale: 0.98 }}
							transition={{ duration: 0.2 }}>
							<Button
								variant="ghost"
								className={cn(
									"w-full justify-start gap-3 rounded-xl h-12 px-4 relative overflow-hidden",
									activeTab === item.id
										? "bg-primary/10 text-primary font-medium"
										: "hover:bg-muted/50",
									isCollapsed ? "justify-center" : ""
								)}
								onClick={() => handleTabChange(item.id)}>
								{activeTab === item.id && (
									<motion.div
										layoutId="activeTab"
										className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-full"
										transition={{ duration: 0.3 }}
									/>
								)}
								<item.icon
									size={20}
									className={activeTab === item.id ? "text-primary" : ""}
								/>
								<AnimatePresence mode="wait">
									{!isCollapsed && (
										<motion.span
											// initial={{ opacity: 0, width: 0 }}
											// animate={{ opacity: 1, width: "auto" }}
											// exit={{ opacity: 0, width: 0 }}
											// transition={{ duration: 0.3 }}
											className="whitespace-nowrap overflow-hidden">
											{item.label}
										</motion.span>
									)}
								</AnimatePresence>
							</Button>
						</motion.div>
					))}
				</div>
			</div>

			<div className="px-3 mt-auto">
				<div
					className={cn(
						"rounded-xl p-4 bg-muted/50 border border-border/50",
						isCollapsed ? "p-2" : ""
					)}>
					{!isCollapsed ? (
						<div className="flex flex-col space-y-2">
							<p className="text-sm font-medium">Need help?</p>
							<p className="text-xs text-muted-foreground">
								Check our documentation or contact support
							</p>
							<Button size="sm" variant="default" className="mt-2 rounded-lg">
								<Settings className="h-4 w-4 mr-2" />
								Settings
							</Button>
						</div>
					) : (
						<Button size="icon" variant="ghost" className="w-full h-10">
							<Settings className="h-5 w-5" />
						</Button>
					)}
				</div>
			</div>

			{/* Toggle button for desktop */}
			<div className="hidden md:block absolute -right-3 top-8">
				<Button
					variant="outline"
					size="icon"
					onClick={toggleSidebar}
					className="h-6 w-6 rounded-full border border-border bg-background shadow-md">
					{isCollapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
				</Button>
			</div>
		</motion.div>
	);

	// Mobile sidebar
	const MobileSidebar = () => (
		<motion.div
			className="fixed top-16 left-0 z-20 h-[calc(100vh-4rem)] w-[280px] bg-background/95 backdrop-blur-md border-r border-border/50 flex flex-col"
			variants={mobileSidebarVariants}
			initial="closed"
			animate={isMobileOpen ? "open" : "closed"}>
			{/* <div className="absolute top-4 right-4">
				<Button
					variant="ghost"
					size="icon"
					onClick={() => setIsMobileOpen(false)}
					className="rounded-full h-8 w-8">
					<ChevronLeft size={16} />
				</Button>
			</div> */}

			<div className="flex-1 overflow-y-auto px-3 py-10 space-y-6">
				<div className="space-y-1.5">
					{menuItems.map((item) => (
						<motion.div
							key={item.id}
							whileHover={{ x: 4 }}
							whileTap={{ scale: 0.98 }}
							transition={{ duration: 0.2 }}>
							<Button
								variant="ghost"
								className={cn(
									"w-full justify-start gap-3 rounded-xl h-12 px-4 relative overflow-hidden",
									activeTab === item.id
										? "bg-primary/10 text-primary font-medium"
										: "hover:bg-muted/50"
								)}
								onClick={() => handleTabChange(item.id)}>
								{activeTab === item.id && (
									<motion.div
										layoutId="mobileActiveTab"
										className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-full"
										transition={{ duration: 0.3 }}
									/>
								)}
								<item.icon
									size={20}
									className={activeTab === item.id ? "text-primary" : ""}
								/>
								<span className="whitespace-nowrap overflow-hidden">
									{item.label}
								</span>
							</Button>
						</motion.div>
					))}
				</div>
			</div>

			<div className="px-3 mt-auto pb-6">
				<div className="rounded-xl p-4 bg-muted/50 border border-border/50">
					<div className="flex flex-col space-y-2">
						<p className="text-sm font-medium">Need help?</p>
						<p className="text-xs text-muted-foreground">
							Check our documentation or contact support
						</p>
						<Button size="sm" variant="default" className="mt-2 rounded-lg">
							<Settings className="h-4 w-4 mr-2" />
							Settings
						</Button>
					</div>
				</div>
			</div>
		</motion.div>
	);

	return (
		<>
			{/* Mobile overlay */}
			<AnimatePresence>
				{isMobile && isMobileOpen && (
					<motion.div
						initial={{ opacity: 0 }}
						animate={{ opacity: 0.6 }}
						exit={{ opacity: 0 }}
						transition={{ duration: 0.3 }}
						className="fixed inset-0 top-16 bg-black z-10 backdrop-blur-sm"
						onClick={() => setIsMobileOpen(false)}
					/>
				)}
			</AnimatePresence>

			{/* Render appropriate sidebar based on device */}
			{isMobile ? <MobileSidebar /> : <DesktopSidebar />}
		</>
	);
}
