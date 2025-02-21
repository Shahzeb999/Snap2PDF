import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageGrab
from datetime import datetime
import os
import threading
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import time
import subprocess

class ZoomSnap:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Zoom Snap")
        
        # Make window floating and always on top
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Create screenshots directory in the same folder as the script
        self.screenshot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Screenshots")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        self.screenshot_paths = []
        self.create_ui()
        
        # Variables for window dragging
        self.x = None
        self.y = None
        
    def create_ui(self):
        # Create main frame
        self.frame = ttk.Frame(self.root, padding="5")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add handle for dragging
        self.handle = ttk.Label(self.frame, text="≡ Zoom Snap")
        self.handle.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.handle.bind('<Button-1>', self.start_drag)
        self.handle.bind('<B1-Motion>', self.on_drag)
        
        # Screenshot button
        self.screenshot_btn = ttk.Button(
            self.frame, 
            text="📸 Capture",
            command=self.take_screenshot
        )
        self.screenshot_btn.grid(row=1, column=0, padx=2)
        
        # Save PDF button
        self.save_btn = ttk.Button(
            self.frame,
            text="💾 Save PDF",
            command=self.save_pdf
        )
        self.save_btn.grid(row=1, column=1, padx=2)
        
        # Open folder button
        self.folder_btn = ttk.Button(
            self.frame,
            text="📁",
            width=3,
            command=self.open_save_folder
        )
        self.folder_btn.grid(row=1, column=2, padx=2)
        
        # Close button
        self.close_btn = ttk.Button(
            self.frame,
            text="✕",
            width=3,
            command=self.root.quit
        )
        self.close_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Status label with smaller font for path
        self.status_label = ttk.Label(self.frame, text="Ready")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=5)
        
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
        
    def on_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def open_save_folder(self):
        """Open the screenshots folder in file explorer"""
        if os.name == 'nt':  # Windows
            os.startfile(self.screenshot_dir)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.run(['open' if os.name == 'darwin' else 'xdg-open', self.screenshot_dir])
        
    def take_screenshot(self):
        def capture():
            # Brief delay to let user prepare
            time.sleep(0.5)
            
            # Instead of minimizing, we'll temporarily hide the window
            self.root.withdraw()
            time.sleep(0.5)  # Wait for window to hide
            
            try:
                # Take the screenshot
                screenshot = ImageGrab.grab()
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(self.screenshot_dir, filename)
                
                # Save the screenshot
                screenshot.save(filepath)
                self.screenshot_paths.append(filepath)
                
                # Update status
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Captured: {len(self.screenshot_paths)} screenshots\nSaving to: {self.screenshot_dir}"
                ))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Error: {str(e)}"
                ))
            finally:
                # Restore the window
                self.root.after(0, self.root.deiconify)
        
        # Run screenshot capture in separate thread
        threading.Thread(target=capture).start()

    def cleanup_screenshots(self):
        """Delete all screenshot files after they've been saved to PDF"""
        for filepath in self.screenshot_paths:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
        
    def save_pdf(self):
        if not self.screenshot_paths:
            self.status_label.config(text="No screenshots to save!")
            return
            
        try:
            # Generate PDF filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = os.path.join(self.screenshot_dir, f"meeting_notes_{timestamp}.pdf")
            
            # Create PDF
            c = canvas.Canvas(pdf_path, pagesize=letter)
            
            for img_path in self.screenshot_paths:
                img = Image.open(img_path)
                # Scale image to fit on page while maintaining aspect ratio
                img_width, img_height = img.size
                aspect = img_height / float(img_width)
                # Use almost full page width
                pdf_width = 500
                pdf_height = pdf_width * aspect
                
                # Add image to PDF
                c.drawImage(img_path, 50, letter[1] - pdf_height - 50,
                           width=pdf_width, height=pdf_height)
                c.showPage()
                
            c.save()
            
            # Delete the individual screenshots
            self.cleanup_screenshots()
            
            # Update status and clear screenshot list
            self.status_label.config(text=f"PDF saved and screenshots cleaned up")
            self.screenshot_paths = []
            
            # Open the folder
            self.open_save_folder()
            
        except Exception as e:
            self.status_label.config(text=f"Error saving PDF: {str(e)}")
        
    def run(self):
        # Position window in top-right corner initially
        self.root.geometry('+{}+{}'.format(
            self.root.winfo_screenwidth() - 200,
            50
        ))
        self.root.mainloop()

if __name__ == "__main__":
    app = ZoomSnap()
    app.run()