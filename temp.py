"""
VyapaarMitra AI - Desktop Prototype
Run in Anaconda Spyder using F5.

Install if needed:
pip install pandas matplotlib pillow

Uses synthetic sample data. No live AI, OCR or payment API.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date, timedelta
import random
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


# ---------------- THEME ----------------

BG = "#050D1C"
PANEL = "#0B172A"
PANEL2 = "#101C32"
BORDER = "#283951"
WHITE = "#F3F2EE"
MUTED = "#AAB6C8"
PURPLE = "#B99AFB"
PURPLE_DARK = "#8B6BE8"
MINT = "#9AD9BC"
RED = "#F08A91"


# ---------------- SAMPLE DATA ----------------

def build_demo_data():
    random.seed(12)
    rows = []
    today = date.today()

    products = {
        "Tea & Coffee": (35, 85),
        "Snacks": (20, 120),
        "Groceries": (45, 260),
        "Cold Drinks": (25, 70),
        "Household": (60, 320)
    }

    for i in range(90):
        day = today - timedelta(days=89 - i)

        for _ in range(random.randint(7, 15)):
            category = random.choice(list(products))
            low, high = products[category]
            amount = random.randint(low, high)

            if day.weekday() >= 5:
                amount = int(amount * 1.15)

            rows.append({
                "Date": pd.Timestamp(day),
                "Transaction ID": "TXN{}".format(10000 + len(rows)),
                "Product Category": category,
                "Amount (₹)": amount,
                "Customer Type": random.choices(
                    ["Returning", "New"],
                    weights=[0.62, 0.38],
                    k=1
                )[0],
                "Payment Method": random.choice(
                    ["UPI", "Cash", "Card"]
                ),
                "Status": random.choices(
                    ["Success", "Review"],
                    weights=[0.96, 0.04],
                    k=1
                )[0]
            })

    return pd.DataFrame(rows)


# ---------------- MAIN APPLICATION ----------------

class VyapaarMitraApp:

    def __init__(self, root):
        self.root = root
        self.root.title("VyapaarMitra AI | Merchant Assistant")
        self.root.geometry("1300x850")
        self.root.minsize(980, 650)
        self.root.configure(bg=BG)

        self.df = build_demo_data()
        self.filtered = self.df.copy()
        self.chat_history = []
        self.uploaded_path = None

        self.setup_styles()
        self.build_layout()
        self.show_page("Overview")

    # ---------------- STYLES ----------------

    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=27,
            bordercolor=BORDER
        )

        style.configure(
            "Treeview.Heading",
            background=PANEL2,
            foreground=PURPLE,
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#34265A")]
        )

        style.configure(
            "TCombobox",
            fieldbackground=PANEL,
            background=PANEL2,
            foreground=WHITE,
            arrowcolor=PURPLE
        )

    # ---------------- MAIN LAYOUT ----------------

    def build_layout(self):
        header = tk.Frame(self.root, bg=BG, padx=22, pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="VyapaarMitra",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 25, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text=" AI",
            bg=BG,
            fg=PURPLE,
            font=("Segoe UI", 25, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="Your AI teammate for a smarter, safer business.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=18, pady=(9, 0))

        tk.Label(
            header,
            text="DEMO MODE",
            bg="#211B3B",
            fg=PURPLE,
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=6
        ).pack(side="right")

        body = tk.Frame(self.root, bg=BG)
        body.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        self.sidebar = tk.Frame(
            body,
            bg=PANEL2,
            width=220,
            padx=12,
            pady=15
        )
        self.sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 14)
        )
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            bg=PANEL2,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=8, pady=(3, 12))

        self.nav_buttons = {}

        pages = [
            ("Overview", "Overview"),
            ("Understand Sales", "Understand Sales"),
            ("Grow Business", "Grow Business"),
            ("MitraVerify", "MitraVerify"),
            ("Ask Assistant", "Ask VyapaarMitra")
        ]

        for label, page in pages:
            button = tk.Button(
                self.sidebar,
                text=label,
                anchor="w",
                command=lambda p=page: self.show_page(p),
                bg=PANEL2,
                fg=WHITE,
                activebackground="#211B3B",
                activeforeground=PURPLE,
                relief="flat",
                bd=0,
                padx=12,
                pady=11,
                font=("Segoe UI", 10)
            )
            button.pack(fill="x", pady=2)
            self.nav_buttons[page] = button

        tk.Frame(
            self.sidebar,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=17)

        tk.Label(
            self.sidebar,
            text="YOUR BUSINESS,\nUNDERSTOOD.",
            bg=PANEL2,
            fg=PURPLE,
            justify="left",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=8)

        tk.Label(
            self.sidebar,
            text=(
                "Sample data only.\n"
                "Payment screenshots are not\n"
                "proof of settlement."
            ),
            bg=PANEL2,
            fg=MUTED,
            justify="left",
            font=("Segoe UI", 9),
            wraplength=175
        ).pack(anchor="w", padx=8, pady=10)

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def page_heading(self, title, subtitle):
        tk.Label(
            self.content,
            text=title,
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w", pady=(2, 3))

        tk.Label(
            self.content,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 16))

    def card(self, parent, title, value, note, accent=MINT):
        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=12,
            pady=12
        )

        tk.Label(
            frame,
            text=title.upper(),
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=value,
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(5, 1))

        tk.Label(
            frame,
            text=note,
            bg=PANEL,
            fg=accent,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        return frame

    # ---------------- CHARTS ----------------

    def make_chart(self, parent):
        fig = Figure(
            figsize=(5.5, 3),
            dpi=100,
            facecolor=PANEL
        )

        ax = fig.add_subplot(111)
        ax.set_facecolor(PANEL)

        for spine in ax.spines.values():
            spine.set_color(BORDER)

        ax.tick_params(colors=MUTED, labelsize=8)
        ax.grid(axis="y", color=BORDER, alpha=0.7)

        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        return fig, ax, canvas

    # ---------------- PAGE NAVIGATION ----------------

    def show_page(self, page):
        self.current_page = page
        self.clear_content()

        for name, button in self.nav_buttons.items():
            button.configure(
                bg="#211B3B" if name == page else PANEL2,
                fg=PURPLE if name == page else WHITE
            )

        if page == "Overview":
            self.page_overview()

        elif page == "Understand Sales":
            self.page_sales()

        elif page == "Grow Business":
            self.page_growth()

        elif page == "MitraVerify":
            self.page_verify()

        else:
            self.page_chat()

    # ---------------- OVERVIEW PAGE ----------------

    def page_overview(self):
        self.page_heading(
            "Business overview",
            "A quick view of your store's sample performance."
        )

        revenue = int(self.filtered["Amount (₹)"].sum())
        count = len(self.filtered)
        average = revenue / max(count, 1)

        returning = (
            self.filtered["Customer Type"].eq("Returning").mean() * 100
            if count else 0
        )

        metrics = tk.Frame(self.content, bg=BG)
        metrics.pack(fill="x", pady=(0, 14))

        metric_data = [
            (
                "Sales revenue",
                "₹{:,.0f}".format(revenue),
                "Selected sample period",
                PURPLE
            ),
            (
                "Transactions",
                "{:,}".format(count),
                "Sample records",
                MINT
            ),
            (
                "Average bill",
                "₹{:,.0f}".format(average),
                "Revenue per transaction",
                PURPLE
            ),
            (
                "Returning customers",
                "{:.1f}%".format(returning),
                "Share of transactions",
                MINT
            )
        ]

        for i, item in enumerate(metric_data):
            metric = self.card(metrics, *item)
            metric.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=5
            )
            metrics.grid_columnconfigure(i, weight=1)

        charts = tk.Frame(self.content, bg=BG)
        charts.pack(fill="both", expand=True)

        left = tk.Frame(
            charts,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=10,
            pady=10
        )

        right = tk.Frame(
            charts,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=10,
            pady=10
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            left,
            text="Sales over time",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            right,
            text="Sales by category",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        daily = self.filtered.groupby("Date")[
            "Amount (₹)"
        ].sum().sort_index()

        fig, ax, canvas = self.make_chart(left)

        ax.plot(
            daily.index,
            daily.values,
            color=PURPLE_DARK,
            linewidth=2.4
        )

        ax.fill_between(
            daily.index,
            daily.values,
            color=PURPLE_DARK,
            alpha=0.14
        )

        fig.autofmt_xdate()
        canvas.draw()

        cat = self.filtered.groupby(
            "Product Category"
        )["Amount (₹)"].sum().sort_values(ascending=False)

        fig2, ax2, canvas2 = self.make_chart(right)

        ax2.bar(
            cat.index,
            cat.values,
            color=[
                PURPLE_DARK,
                MINT,
                "#7164A8",
                "#7294B5",
                "#B99AFB"
            ]
        )

        ax2.tick_params(axis="x", rotation=25)
        ax2.set_ylabel("Sales (₹)", color=MUTED)
        canvas2.draw()

        best = cat.index[0] if len(cat) else "N/A"

        tk.Label(
            self.content,
            text=(
                "INSIGHT  •  {} is the highest-sales category "
                "in the current sample data.".format(best)
            ),
            bg=BG,
            fg=MINT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=12)

    # ---------------- SALES PAGE ----------------

    def page_sales(self):
        self.page_heading(
            "Understand sales",
            "Explore product categories, customers and transaction records."
        )

        cat = self.filtered.groupby("Product Category").agg(
            Sales=("Amount (₹)", "sum"),
            Transactions=("Transaction ID", "count"),
            Average_Bill=("Amount (₹)", "mean")
        ).sort_values(
            "Sales",
            ascending=False
        ).reset_index()

        chart_panel = tk.Frame(
            self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=12,
            pady=10
        )

        chart_panel.pack(fill="x", pady=(0, 12))

        tk.Label(
            chart_panel,
            text="Category performance",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        fig, ax, canvas = self.make_chart(chart_panel)

        ax.bar(
            cat["Product Category"],
            cat["Sales"],
            color=PURPLE_DARK
        )

        ax.set_ylabel("Sales (₹)", color=MUTED)
        ax.tick_params(axis="x", rotation=15)
        canvas.draw()

        tk.Label(
            self.content,
            text="Recent transactions",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(2, 6))

        table_frame = tk.Frame(self.content, bg=BG)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "Date",
            "Transaction ID",
            "Product Category",
            "Amount (₹)",
            "Customer Type",
            "Payment Method",
            "Status"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        widths = {
            "Date": 100,
            "Transaction ID": 125,
            "Product Category": 150,
            "Amount (₹)": 100,
            "Customer Type": 125,
            "Payment Method": 120,
            "Status": 90
        }

        for col in columns:
            tree.heading(col, text=col)
            tree.column(
                col,
                width=widths[col],
                minwidth=80,
                anchor="w",
                stretch=False
            )

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        # Horizontal scrollbar
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(
            row=1, column=0, sticky="ew"
        )

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        latest = self.filtered.sort_values(
            "Date",
            ascending=False
        ).head(100)

        for _, row in latest.iterrows():
            tree.insert(
                "",
                "end",
                values=(
                    row["Date"].strftime("%d %b %Y"),
                    row["Transaction ID"],
                    row["Product Category"],
                    "₹{:,.0f}".format(row["Amount (₹)"]),
                    row["Customer Type"],
                    row["Payment Method"],
                    row["Status"]
                )
            )

        tk.Button(
            self.content,
            text="Export filtered data to CSV",
            command=self.export_csv,
            bg=PURPLE_DARK,
            fg="white",
            activebackground=PURPLE,
            relief="flat",
            padx=12,
            pady=8
        ).pack(anchor="e", pady=9)

    # ---------------- GROW BUSINESS PAGE ----------------

    def page_growth(self):
        self.page_heading(
            "Grow your business",
            "Create a campaign using sample sales data."
        )

        # Campaign form is placed first so the button is visible.
        form = tk.Frame(
            self.content,
            bg=PANEL2,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=15,
            pady=13
        )

        form.pack(fill="x", pady=(0, 12))

        tk.Label(
            form,
            text="Create a campaign idea",
            bg=PANEL2,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 9)
        )

        tk.Label(
            form,
            text="Audience",
            bg=PANEL2,
            fg=MUTED
        ).grid(row=1, column=0, sticky="w", pady=5)

        audience = ttk.Combobox(
            form,
            values=[
                "Returning customers",
                "New customers",
                "All customers"
            ],
            state="readonly",
            width=28
        )

        audience.current(0)
        audience.grid(
            row=1, column=1,
            sticky="w", padx=10, pady=5
        )

        tk.Label(
            form,
            text="Goal",
            bg=PANEL2,
            fg=MUTED
        ).grid(row=2, column=0, sticky="w", pady=5)

        goal = ttk.Combobox(
            form,
            values=[
                "Increase evening sales",
                "Encourage repeat visits",
                "Move slow-selling stock",
                "Increase average bill"
            ],
            state="readonly",
            width=28
        )

        goal.current(0)
        goal.grid(
            row=2, column=1,
            sticky="w", padx=10, pady=5
        )

        result = tk.Label(
            form,
            text="",
            bg=PANEL2,
            fg=MINT,
            wraplength=650,
            justify="left"
        )

        result.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(8, 0)
        )

        def generate():
            selected_audience = audience.get()
            selected_goal = goal.get()

            result.config(
                text=(
                    "Campaign idea: Target "
                    + selected_audience.lower()
                    + " to "
                    + selected_goal.lower()
                    + ". Run a short test, record sales and "
                    "redemptions, and compare with a similar "
                    "period. Check profit margins before publishing."
                )
            )

        tk.Button(
            form,
            text="Generate campaign idea",
            command=generate,
            bg=PURPLE_DARK,
            fg="white",
            activebackground=PURPLE,
            relief="flat",
            padx=12,
            pady=7
        ).grid(
            row=3,
            column=1,
            sticky="w",
            padx=10,
            pady=8
        )

        # Recommendations
        cat = self.filtered.groupby(
            "Product Category"
        )["Amount (₹)"].sum().sort_values(ascending=False)

        best = cat.index[0] if len(cat) else "No data"
        slow = cat.index[-1] if len(cat) else "No data"

        returning = (
            self.filtered["Customer Type"].eq("Returning").mean() * 100
            if len(self.filtered) else 0
        )

        recommendations = [
            (
                "Build on what works",
                "{} leads sales in this sample. Check stock levels "
                "before promoting it.".format(best)
            ),
            (
                "Test a focused offer",
                "Try a small bundle involving {} and compare "
                "sales and margins.".format(slow)
            ),
            (
                "Encourage repeat visits",
                "{:.1f}% of sample transactions are from returning "
                "customers. Test a repeat-visit offer.".format(returning)
            )
        ]

        for title, description in recommendations:
            panel = tk.Frame(
                self.content,
                bg=PANEL,
                highlightbackground=BORDER,
                highlightthickness=1,
                padx=12,
                pady=10
            )

            panel.pack(fill="x", pady=5)

            tk.Label(
                panel,
                text=title,
                bg=PANEL,
                fg=PURPLE,
                font=("Segoe UI", 11, "bold")
            ).pack(anchor="w")

            tk.Label(
                panel,
                text=description,
                bg=PANEL,
                fg=WHITE,
                font=("Segoe UI", 9),
                wraplength=700,
                justify="left"
            ).pack(anchor="w", pady=(4, 0))

    # ---------------- MITRAVERIFY PAGE ----------------

    def page_verify(self):
        self.page_heading(
            "MitraVerify",
            "Payment screenshot review and risk-awareness checklist."
        )

        warning = tk.Frame(
            self.content,
            bg="#2A1726",
            highlightbackground="#704050",
            highlightthickness=1,
            padx=14,
            pady=12
        )

        warning.pack(fill="x", pady=(0, 12))

        tk.Label(
            warning,
            text="IMPORTANT: A screenshot is not proof of payment settlement.",
            bg="#2A1726",
            fg=RED,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            warning,
            text=(
                "Confirm payment in your authorised merchant account "
                "or transaction history."
            ),
            bg="#2A1726",
            fg=WHITE,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 0))

        upload_panel = tk.Frame(
            self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=15,
            pady=14
        )

        upload_panel.pack(fill="x", pady=(0, 12))

        tk.Label(
            upload_panel,
            text="Upload a payment screenshot",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        self.image_label = tk.Label(
            upload_panel,
            text="No image selected",
            bg=PANEL,
            fg=MUTED,
            pady=10
        )

        self.image_label.pack(anchor="w")

        def choose_image():
            path = filedialog.askopenfilename(
                title="Choose payment screenshot",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.webp"),
                    ("All files", "*.*")
                ]
            )

            if not path:
                return

            self.uploaded_path = path

            if Image is not None and ImageTk is not None:
                try:
                    img = Image.open(path)
                    img.thumbnail((360, 220))
                    photo = ImageTk.PhotoImage(img)

                    self.image_label.configure(
                        image=photo,
                        text=""
                    )

                    self.image_label.image = photo

                except Exception:
                    self.image_label.configure(
                        text="Image selected: " + path,
                        image=""
                    )
            else:
                self.image_label.configure(
                    text=(
                        "Image selected: " + path
                        + "\nInstall Pillow to preview images."
                    ),
                    image=""
                )

            self.verify_status.config(
                text=(
                    "NEEDS VERIFICATION — payment settlement "
                    "has not been checked."
                ),
                fg=RED
            )

        tk.Button(
            upload_panel,
            text="Choose image",
            command=choose_image,
            bg=PURPLE_DARK,
            fg="white",
            relief="flat",
            padx=12,
            pady=7
        ).pack(anchor="w")

        checklist = tk.Frame(
            self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=15,
            pady=12
        )

        checklist.pack(fill="x")

        tk.Label(
            checklist,
            text="Manual verification checklist",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        checks = [
            "Open the official payment app or authorised merchant dashboard.",
            "Find the transaction in the official transaction history.",
            "Compare amount, date/time, reference ID and transaction status.",
            "If details do not match, pause fulfilment and contact the provider."
        ]

        self.check_vars = []

        for item in checks:
            var = tk.BooleanVar(value=False)
            self.check_vars.append(var)

            tk.Checkbutton(
                checklist,
                text=item,
                variable=var,
                bg=PANEL,
                fg=WHITE,
                selectcolor=PANEL2,
                activebackground=PANEL,
                activeforeground=WHITE,
                wraplength=720,
                justify="left"
            ).pack(anchor="w", pady=3)

        self.verify_status = tk.Label(
            checklist,
            text="Status: waiting for review.",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 10, "bold")
        )

        self.verify_status.pack(anchor="w", pady=(10, 0))

        tk.Label(
            self.content,
            text="OCR and payment API integrations are not active.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=10)

    # ---------------- CHAT PAGE ----------------

    def page_chat(self):
        self.page_heading(
            "Ask VyapaarMitra",
            "A simple rule-based assistant for this desktop demo."
        )

        chat_box = tk.Frame(
            self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=12,
            pady=10
        )

        chat_box.pack(fill="both", expand=True)

        self.chat_text = tk.Text(
            chat_box,
            bg=PANEL,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            wrap="word",
            font=("Segoe UI", 10),
            padx=8,
            pady=8,
            state="disabled"
        )

        self.chat_text.pack(fill="both", expand=True)

        self.chat_text.tag_configure(
            "user",
            foreground=PURPLE,
            spacing1=8,
            font=("Segoe UI", 10, "bold")
        )

        self.chat_text.tag_configure(
            "assistant",
            foreground=MINT,
            spacing1=8,
            font=("Segoe UI", 10, "bold")
        )

        if not self.chat_history:
            self.chat_history.append((
                "assistant",
                "Namaste! Ask me about sales, top categories, "
                "returning customers, marketing ideas or payment verification."
            ))

        self.render_chat()

        input_row = tk.Frame(self.content, bg=BG)
        input_row.pack(fill="x", pady=(10, 0))

        self.chat_input = tk.Entry(
            input_row,
            bg=PANEL,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Segoe UI", 11)
        )

        self.chat_input.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=(0, 8)
        )

        self.chat_input.bind(
            "<Return>",
            lambda event: self.send_chat()
        )

        tk.Button(
            input_row,
            text="Send",
            command=self.send_chat,
            bg=PURPLE_DARK,
            fg="white",
            relief="flat",
            padx=20,
            pady=8
        ).pack(side="right")

        tk.Label(
            self.content,
            text="Demo assistant only — no live AI model is connected.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=8)

    def render_chat(self):
        self.chat_text.configure(state="normal")
        self.chat_text.delete("1.0", "end")

        for role, text in self.chat_history:
            if role == "user":
                heading = "YOU\n"
            else:
                heading = "VYAPAARMITRA AI\n"

            self.chat_text.insert("end", heading, role)
            self.chat_text.insert("end", text + "\n\n")

        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")

    def answer_question(self, question):
        q = question.lower()

        sales = int(self.filtered["Amount (₹)"].sum())
        count = len(self.filtered)
        average = sales / max(count, 1)

        returning = (
            self.filtered["Customer Type"].eq("Returning").mean() * 100
            if count else 0
        )

        cats = self.filtered.groupby(
            "Product Category"
        )["Amount (₹)"].sum().sort_values(ascending=False)

        if cats.empty:
            return "There is no sample data available to analyse."

        if any(word in q for word in [
            "best", "top", "highest", "popular", "category"
        ]):
            return (
                "{} is the highest-sales category in this sample, "
                "with ₹{:,.0f} in sales. Check stock before promoting it."
            ).format(cats.index[0], cats.iloc[0])

        if any(word in q for word in [
            "return", "loyal", "repeat", "customer"
        ]):
            return (
                "Returning customers account for {:.1f}% of "
                "transactions in this sample. You could test a "
                "repeat-visit offer."
            ).format(returning)

        if any(word in q for word in [
            "sales", "revenue", "earning", "income"
        ]):
            return (
                "Sample sales total ₹{:,.0f} across {:,} transactions. "
                "Average bill value is ₹{:,.0f}."
            ).format(sales, count, average)

        if any(word in q for word in [
            "payment", "screenshot", "fraud", "upi", "verify"
        ]):
            return (
                "Treat screenshots as risk signals, not proof. "
                "Confirm the transaction status and reference ID "
                "in your authorised merchant account."
            )

        if any(word in q for word in [
            "offer", "marketing", "campaign", "grow", "increase"
        ]):
            return (
                "Consider a small, time-limited test for {}. "
                "Compare sales and margins against a similar period."
            ).format(cats.index[-1])

        return (
            "Try asking about sales revenue, the top category, "
            "returning customers, marketing ideas or payment verification."
        )

    def send_chat(self):
        question = self.chat_input.get().strip()

        if not question:
            return

        self.chat_history.append(("user", question))

        answer = self.answer_question(question)
        self.chat_history.append(("assistant", answer))

        self.chat_input.delete(0, "end")
        self.render_chat()

    # ---------------- CSV EXPORT ----------------

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            title="Save filtered transactions",
            defaultextension=".csv",
            filetypes=[("CSV file", "*.csv")],
            initialfile="vyapaarmitra_sample_transactions.csv"
        )

        if not path:
            return

        try:
            self.filtered.to_csv(path, index=False)

            messagebox.showinfo(
                "Export complete",
                "Sample data exported successfully."
            )

        except Exception as exc:
            messagebox.showerror(
                "Export failed",
                str(exc)
            )


# ---------------- RUN PROGRAM ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = VyapaarMitraApp(root)
    root.mainloop()