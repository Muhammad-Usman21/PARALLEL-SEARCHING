import { createSlice } from "@reduxjs/toolkit"

const initialState = {
  theme: localStorage.getItem("theme") || "light",
}

const themeSlice = createSlice({
  name: "theme",
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.theme = state.theme === "light" ? "dark" : "light"
      localStorage.setItem("theme", state.theme)

      // Update the document class for compatibility with the new theme system
      document.documentElement.classList.remove("light", "dark")
      document.documentElement.classList.add(state.theme)
    },
  },
})

export const { toggleTheme } = themeSlice.actions
export default themeSlice.reducer

