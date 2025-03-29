"use client";

import type React from "react";

import { Moon, Sun, Menu, ChevronLeft } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { useTheme } from "@/components/theme-provider";
import { useMediaQuery } from "@/hooks/use-mobile";

export function Header({
	toggleSidebar,
	isMobileOpen,
}: {
	toggleSidebar: () => void;
	isMobileOpen: boolean;
}) {
	const { theme, setTheme } = useTheme();
	const isMobile = useMediaQuery("(max-width: 768px)");
	const navigate = useNavigate();

	const handleLogoClick = (e: React.MouseEvent) => {
		e.preventDefault();
		navigate("/?tab=text");
	};

	return (
		<motion.header
			initial={{ y: -20, opacity: 0 }}
			animate={{ y: 0, opacity: 1 }}
			transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
			className="sticky top-0 z-30 w-full border-b border-border/40 bg-background/80 backdrop-blur-sm">
			<div className="container flex h-16 items-center justify-between">
				<Link
					to="/?tab=text"
					onClick={handleLogoClick}
					className="flex items-center gap-2">
					<motion.div
						whileHover={{ scale: 1.05 }}
						whileTap={{ scale: 0.95 }}
						transition={{ type: "spring", stiffness: 400, damping: 10 }}
						className="relative">
						<div className="absolute -inset-1 rounded-full bg-gradient-to-r from-primary/50 to-primary/20 blur-sm opacity-70"></div>
						<div className="relative w-8 h-8 rounded-full bg-primary flex items-center justify-center">
							<span className="text-primary-foreground font-bold text-sm">
								S
							</span>
						</div>
					</motion.div>
					<motion.span
						className="text-xl font-bold tracking-tight"
						whileHover={{ scale: 1.03 }}
						transition={{ type: "spring", stiffness: 400, damping: 10 }}>
						SEARCHING
					</motion.span>
				</Link>

				<div className="flex items-center gap-2">
					<motion.div
						whileHover={{ scale: 1.05 }}
						whileTap={{ scale: 0.95 }}
						transition={{ duration: 0.2 }}>
						<Button
							variant="ghost"
							size="icon"
							onClick={() => setTheme(theme === "light" ? "dark" : "light")}
							aria-label="Toggle theme"
							className="relative rounded-full bg-muted/50 hover:bg-muted">
							<AnimatePresence mode="wait" initial={false}>
								{theme === "light" ? (
									<motion.div
										key="sun"
										initial={{ opacity: 0, rotate: -90 }}
										animate={{ opacity: 1, rotate: 0 }}
										exit={{ opacity: 0, rotate: 90 }}
										transition={{ duration: 0.2 }}
										className="absolute inset-0 flex items-center justify-center">
										<Sun className="h-5 w-5" />
									</motion.div>
								) : (
									<motion.div
										key="moon"
										initial={{ opacity: 0, rotate: 90 }}
										animate={{ opacity: 1, rotate: 0 }}
										exit={{ opacity: 0, rotate: -90 }}
										transition={{ duration: 0.2 }}
										className="absolute inset-0 flex items-center justify-center">
										<Moon className="h-5 w-5" />
									</motion.div>
								)}
							</AnimatePresence>
							<span className="sr-only">Toggle theme</span>
						</Button>
					</motion.div>

					{isMobile && (
						<motion.div
							whileHover={{ scale: 1.05 }}
							whileTap={{ scale: 0.95 }}
							transition={{
								duration: 0.2,
								type: "spring",
								stiffness: 400,
								damping: 17,
							}}>
							<Button
								variant="ghost"
								size="icon"
								onClick={toggleSidebar}
								aria-label="Toggle menu"
								className="rounded-full bg-muted/50 hover:bg-muted relative">
								<AnimatePresence mode="wait">
									{isMobileOpen ? (
										<motion.div
											key="close"
											initial={{ rotate: -90, opacity: 0 }}
											animate={{ rotate: 0, opacity: 1 }}
											exit={{ rotate: 90, opacity: 0 }}
											transition={{
												duration: 0.3,
												type: "spring",
												stiffness: 300,
												damping: 20,
											}}
											className="absolute inset-0 flex items-center justify-center">
											<ChevronLeft className="h-5 w-5" />
										</motion.div>
									) : (
										<motion.div
											key="menu"
											initial={{ rotate: 90, opacity: 0 }}
											animate={{ rotate: 0, opacity: 1 }}
											exit={{ rotate: -90, opacity: 0 }}
											transition={{
												duration: 0.3,
												type: "spring",
												stiffness: 300,
												damping: 20,
											}}
											className="absolute inset-0 flex items-center justify-center">
											<Menu className="h-5 w-5" />
										</motion.div>
									)}
								</AnimatePresence>
								<span className="sr-only">Toggle menu</span>
							</Button>
						</motion.div>
					)}
				</div>
			</div>
		</motion.header>
	);
}
