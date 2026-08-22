import { create } from 'zustand'

const useStore = create((set) => ({
  // Authentication state
  isAuthenticated: false,
  youtubeChannels: [],
  
  setAuthenticated: (value) => set({ isAuthenticated: value }),
  setYoutubeChannels: (channels) => set({ youtubeChannels: channels }),
  
  // Video generation state
  currentVideo: null,
  generatedVideos: [],
  isGenerating: false,
  generationProgress: 0,
  
  setCurrentVideo: (video) => set({ currentVideo: video }),
  setGeneratedVideos: (videos) => set({ generatedVideos: videos }),
  setIsGenerating: (value) => set({ isGenerating: value }),
  setGenerationProgress: (progress) => set({ generationProgress: progress }),
  
  // UI state
  theme: localStorage.getItem('theme') || 'dark',
  setTheme: (theme) => {
    localStorage.setItem('theme', theme)
    set({ theme })
  }
}))

export default useStore
