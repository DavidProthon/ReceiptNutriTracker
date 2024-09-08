"""
The module used to create different types of graphs
"""

import matplotlib.pyplot as plt
import pandas as pd

#TODO
#add the option to set the time range for displaying in the chart
#def select_required_items insert into process_data

class GraphGenerator:
    def __init__(self,df):
        self.df = df
        self.item_dict = {}
        self.selected_columns = ["Položka", "Datum_nákupu", "Cena", "Velikost_balení", "Poměrová_cena"]
        self.new_df = pd.DataFrame(columns=self.selected_columns)

    def select_required_items(self,items):
        """
        Function iterates through the database and finds all selected items of all selected foods.
        """

        for item in items:
            filtered_df = self.df[self.df["Položka"] == item][self.selected_columns]
            self.item_dict[item] = filtered_df
            
        for item in items:
            filtered_df = self.df[self.df["Položka"] == item][self.selected_columns]
            self.new_df = pd.concat([self.new_df, filtered_df])
    
    def show_line_chart(self,column,y_axis_name,fontsize_xlabel = 14,fontsize_ylabel = 14):
        items = self.new_df["Položka"].unique()
        fig, ax = plt.subplots(figsize=(12, 6),dpi=100)

        for item in items:
            df_filtered = self.new_df[self.new_df["Položka"] == item]
            ax.plot(df_filtered["Datum_nákupu"], df_filtered[column], marker="o", label=item)

        ax.set_xlabel("Datum_nákupu",fontsize=fontsize_xlabel)
        ax.set_ylabel(y_axis_name,fontsize=fontsize_ylabel)
        ax.set_title("Cena položek v čase nákupu")
        ax.legend(title="Položky")
        ax.grid(True)
        ax.tick_params(rotation=45)  
        fig.tight_layout()

        return fig
        
    def show_bar_chart(self,show_items,convert_to_percentages = False,fontsize=10, fontsize_xlabel = 14, fontsize_ylabel = 14, chart_name = None):
        df_filter = self.df[show_items]
        df_grouped = df_filter.groupby("Měsíc").sum(numeric_only=True)

        if convert_to_percentages:
            df_grouped = df_grouped.div(df_grouped.sum(axis=1), axis=0) * 100 
       
        fig, ax = plt.subplots(figsize=(12, 6),dpi=100)

        try:
            df_grouped.plot(kind="bar", stacked=True, ax=ax)
        except TypeError as e:
            return fig 

        ax.set_xlabel("Rok-Měsíc",fontsize=fontsize_xlabel)
        ax.set_ylabel("Průměrné_množství_živin_za_den[g]",fontsize=fontsize_ylabel)
        ax.set_title(chart_name)
        ax.set_xticklabels(df_grouped.index.strftime("%Y-%m"), rotation=45)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=2)

        #Adding column descriptions
        for container in ax.containers:
            for bar in container:
                height = bar.get_height()
                if height > 0:  
                    ax.annotate(f"{height:.0f}",
                                (bar.get_x() + bar.get_width() / 2., bar.get_y() + height / 2),
                                ha="center", va="center", fontsize=fontsize, color="black")
                    
        return fig
    

