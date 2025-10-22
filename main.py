import customtkinter as ctk

# --- 1. EXTERNAL PAGE IMPORTS (Assumed to be in other files) ---
# NOTE: These classes (TextPage, ImagePage, etc.) are assumed to be defined
# in the specified modules and will be imported here.
try:
    # If running in an environment where these modules exist:
    from UI.type_converter.text_converter import TextPage
    from UI.type_converter.image_converter import ImagePage
    from UI.type_converter.audio_converter import AudioPage
    from UI.type_converter.video_converter import VideoPage
except ImportError:
    # Placeholder definitions for a runnable environment if external files are missing
    # In a real app, you would remove this block and ensure the imports above work.
    class TextPage(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="white")
            ctk.CTkLabel(self, text="Text Converter (External File)", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=50)
    class ImagePage(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="white")
            ctk.CTkLabel(self, text="Image Converter (External File)", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=50)
    class AudioPage(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="white")
            ctk.CTkLabel(self, text="Audio Converter (External File)", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=50)
    class VideoPage(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="white")
            ctk.CTkLabel(self, text="Video Converter (External File)", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=50)


# Set CustomTkinter appearance settings
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# --- 2. TOP BAR COMPONENT ---

class TopBar(ctk.CTkFrame):
    """
    A simple navigation bar containing a search field and user profile info.
    """
    def __init__(self, parent):
        # Configure the frame appearance
        super().__init__(parent, fg_color="#f5faff", height=65)
        self.pack_propagate(False) # Prevents the frame from resizing based on content

        # Search Entry Field
        search = ctk.CTkEntry(
            self,
            placeholder_text="Search for a utility tool...",
            width=340,
            corner_radius=12,
            border_color="#dbe8f7",
            fg_color="#ffffff",
            text_color="#333333"
        )
        search.pack(side="left", padx=36, pady=14)

        # User Profile Display
        user_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=15)
        user_frame.pack(side="right", padx=26)

        # Status Indicator
        ctk.CTkLabel(
            user_frame, text="🟢", font=ctk.CTkFont(size=22), fg_color="transparent"
        ).pack(side="left")

        # Username Label
        ctk.CTkLabel(
            user_frame, text="ABC",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#236fff", fg_color="transparent"
        ).pack(side="left", padx=9)


# --- 3. SIDEBAR COMPONENT ---

class Sidebar(ctk.CTkFrame):
    """
    The main navigation panel with expandable dropdowns.
    """
    def __init__(self, parent, show_page_callback):
        # Initialize the Sidebar frame
        super().__init__(parent, width=245, fg_color="#f0f6ff", corner_radius=0)
        self.show_page_callback = show_page_callback
        self.is_expanded = False # State to track dropdown visibility

        # Title/Logo Label
        ctk.CTkLabel(
            self, text="UTILITY TOOLS", font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#236fff", fg_color="transparent"
        ).pack(pady=(25, 22), padx=18, anchor="w")

        # --- File Conversion Section (Expandable) ---
        self.converter_section_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.converter_section_frame.pack(fill="x")

        # Main Dropdown Button
        self.converter_btn = ctk.CTkButton(
            self.converter_section_frame,
            text="File Conversion Tools ▼",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#e8f0fe",
            text_color="#236fff",
            hover_color="#d3e3fd",
            anchor="w",
            corner_radius=8,
            command=self.toggle_dropdown # Toggles expansion
        )
        self.converter_btn.pack(fill="x", padx=18)

        # Frame to hold the actual dropdown items (initially empty/unpacked)
        self.dropdown_frame = ctk.CTkFrame(self.converter_section_frame, fg_color="transparent")

        # Create dropdown buttons and store them
        self.dropdown_buttons = {}
        dropdown_items = [("Text", "text"), ("Image", "image"), ("Audio", "audio"), ("Video", "video")]

        for name, key in dropdown_items:
            btn = ctk.CTkButton(
                self.dropdown_frame, text=name, font=ctk.CTkFont(size=13),
                fg_color="#f8fbfe", text_color="#236fff", hover_color="#c2e6fb",
                anchor="w", corner_radius=8,
                command=lambda k=key: self.on_dropdown_click(k)
            )
            self.dropdown_buttons[key] = btn

        # --- Other Sidebar Categories (Non-Expandable) ---
        other_categories = [
            "Image Utility", "Document Utility", "Text & Data Tools",
            "Media Tools", "File & Utility Tools", "Web & Network Tools",
            "Security & Privacy Tools", "Developer Utilities", "Others",
        ]
        
        # NOTE: For simplicity, these buttons currently link to placeholder pages
        # The logic below demonstrates how to create unexpandable navigation buttons
        for cat in other_categories:
            # Determine a placeholder page key (just for demo purposes)
            page_key = "text" if cat in ["Document Utility", "Text & Data Tools"] else "image"
            
            btn = ctk.CTkButton(
                self, text=cat, font=ctk.CTkFont(size=13),
                fg_color="transparent", text_color="#69a1f2", hover_color="#d0e2ff",
                anchor="w", corner_radius=0,
                command=lambda p=page_key: self.show_page_callback(p)
            )
            # Use smaller padding for non-dropdown items to look like a list
            btn.pack(padx=35, pady=3, fill="x") 


    def toggle_dropdown(self):
        """Toggles the visibility of the dropdown menu items."""
        if self.is_expanded:
            # Collapse the menu
            for btn in self.dropdown_buttons.values():
                btn.pack_forget() # Remove buttons
            self.dropdown_frame.pack_forget() # Remove the container frame
            self.converter_btn.configure(text="File Conversion Tools ▼")
        else:
            # Expand the menu
            self.dropdown_frame.pack(fill="x", padx=30, pady=(0, 12)) # Pack container frame
            for btn in self.dropdown_buttons.values():
                btn.pack(fill="x", pady=3) # Pack individual buttons
            self.converter_btn.configure(text="File Conversion Tools ▲")
            
        self.is_expanded = not self.is_expanded # Update the state


    def on_dropdown_click(self, page_key):
        """
        Handles page navigation when a dropdown item is clicked.
        The dropdown will remain open after selection.
        """
        # 1. Show the selected page content
        self.show_page_callback(page_key)


# --- 4. MAIN DASHBOARD APPLICATION ---

class Dashboard(ctk.CTk):
    """
    The main application window, managing layout and page switching.
    """
    def __init__(self):
        super().__init__()
        self.title("CustomTkinter Utility Dashboard")
        self.geometry("1100x700")
        self.configure(bg="#f5faff") # Background color for the root window

        # Dictionary mapping page keys to their respective classes,
        # using the imported classes.
        self.pages = {
            "text": TextPage,
            "image": ImagePage,
            "audio": AudioPage,
            "video": VideoPage,
        }

        self.current_page = None
        
        # --- Build Layout ---
        
        # 1. Sidebar (Left)
        self.sidebar_frame = Sidebar(self, self.show_page)
        self.sidebar_frame.pack(side="left", fill="y")

        # 2. Topbar (Top)
        self.topbar_frame = TopBar(self)
        self.topbar_frame.pack(side="top", fill="x")

        # 3. Main content area (Right/Center)
        # This frame acts as the container where all content pages are displayed
        self.content_frame = ctk.CTkFrame(
            self, fg_color="#ffffff", # White background for content
            corner_radius=16, # Slightly rounded corners
            border_width=1, # Light border for separation
            border_color="#e0e0e0"
        )
        self.content_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(0, 36), # Space on the right
            pady=36 # Space on the top/bottom
        )

        # Load the default page on startup
        self.show_page("text")

    def show_page(self, page_name):
        """
        Switches the content displayed in the main content frame.
        """
        # Destroy the previous page widget, if one exists
        if self.current_page is not None:
            self.current_page.destroy()
            
        # Get the class for the requested page
        page_class = self.pages.get(page_name)
        
        if page_class:
            # Instantiate the new page and pack it to fill the content area
            self.current_page = page_class(self.content_frame)
            self.current_page.pack(fill="both", expand=True)

# --- 5. APPLICATION ENTRY POINT ---

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
