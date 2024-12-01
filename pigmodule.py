import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_vehicle_proportion_heatmap(data, title='Heatmap of Vehicle Type Proportions by Road Type'):
    """
    根据车辆比例绘制热力图。
    
    参数：
        data (pd.DataFrame): 包含交通数据的 DataFrame。
        group_by (str): 按此列进行分组，默认是 'road_name'。
        title (str): 图表标题，默认是 'Heatmap of Vehicle Type Proportions by Road Type'。
    """
    # 确保涉及的列名存在于 DataFrame 中
    # 绘制热力图
    plt.figure(figsize=(10, 6))
    sns.heatmap(data, annot=True, cmap='YlGnBu', fmt='.2f', cbar=True)
    
    plt.title(title)
    plt.xlabel('Vehicle Types')
    plt.ylabel('Road Types')
    plt.xticks(ticks=range(len(data.columns)), labels=[
        'Pedal Cycles', 'Two-Wheeled Motor Vehicles', 'Cars and Taxis',
        'Buses and Coaches', 'LGVs', 'All HGVs'], rotation=30)
    
    plt.tight_layout()
    plt.show()


    
    
    
def plot_vehicle_ratios(data, vehicle_type, start_year=2000, end_year=2023, exclude_years=None):
    """
    绘制按年份分组的指定车辆比例变化折线图。

    Parameters:
        data (pd.DataFrame): 包含车辆数据的 DataFrame。
        vehicle_type (str): 要分析的车辆类型（列名）。
        start_year (int): 分析开始年份。
        end_year (int): 分析结束年份。
        exclude_years (list): 需要排除的年份。
    """
    if exclude_years is None:
        exclude_years = []
    
    # 按道路类型和年份分组，计算车辆数量及总车辆数量
    yearly_totals = data.groupby(['road_name', 'year']).agg({
        vehicle_type: 'sum',
        'total_vehicles': 'sum'
    }).reset_index()
    
   
    # 计算指定车辆的比例
    yearly_totals[f'{vehicle_type}_ratio'] = (
        yearly_totals[vehicle_type] / yearly_totals['total_vehicles']
    )
    
    # 创建所有道路类型和年份的完整组合
    all_years = range(start_year, end_year +1)
    road_types = yearly_totals['road_name'].unique()
    complete_index = pd.MultiIndex.from_product(
        [road_types, all_years], names=['road_name', 'year']
    )

    # 重新索引数据，确保每个组合都存在
    yearly_totals = yearly_totals.set_index(['road_name', 'year']).reindex(complete_index).reset_index()

    # 将指定年份的数据设置为空
    yearly_totals.loc[yearly_totals['year'].isin(exclude_years), f'{vehicle_type}_ratio'] = None
    
    # 使用线性插值填充缺失值
    yearly_totals[f'{vehicle_type}_ratio'] = yearly_totals.groupby('road_name')[f'{vehicle_type}_ratio'].transform(
        lambda x: x.interpolate(method='linear')
    )
    
    # 创建折线图
    plt.figure(figsize=(10, 6))
    for road_type in yearly_totals['road_name'].unique():
        road_data = yearly_totals[yearly_totals['road_name'] == road_type]
        plt.plot(road_data['year'], road_data[f'{vehicle_type}_ratio'], marker='o', label=f'Road {road_type}')
    
    # 添加图例和标签
    plt.title(f'Yearly Changes in {vehicle_type.capitalize()} Ratios by Road Type')
    plt.xlabel('Year')
    plt.ylabel(f'{vehicle_type.capitalize()} Ratio')
    plt.legend(title='Road Type')
    plt.grid(True)
    
    # 显示图像
    plt.tight_layout()
    plt.show()




def plot_stacked_vehicle_proportions(aggregated_data, vehicle_ratio_columns=None, title='Vehicle Type Proportions by Road Type (Stacked Bar Chart)', figsize=(12, 8)):
    """
    根据指定的车辆比例列绘制堆叠条形图。

    参数：
        aggregated_data (pd.DataFrame): 包含按道路类型和比例的交通数据。
        vehicle_ratio_columns (list): 需要绘制的车辆比例列，默认是 [
            'pedal_cycles_ratio', 'two_wheeled_motor_vehicles_ratio', 'cars_and_taxis_ratio',
            'buses_and_coaches_ratio', 'lgvs_ratio', 'all_hgvs_ratio'
        ]。
        title (str): 图表标题，默认是 'Vehicle Type Proportions by Road Type (Stacked Bar Chart)'。
        figsize (tuple): 图表的尺寸，默认为 (12, 8)。

    返回：
        None
    """
    if vehicle_ratio_columns is None:
        vehicle_ratio_columns = [
            'pedal_cycles_ratio', 'two_wheeled_motor_vehicles_ratio', 'cars_and_taxis_ratio',
            'buses_and_coaches_ratio', 'lgvs_ratio', 'all_hgvs_ratio'
        ]

    # 创建长格式数据，方便堆叠
    stacked_data = aggregated_data[['road_name'] + vehicle_ratio_columns]

    # 将比例列按道路类型堆叠
    stacked_data.set_index('road_name', inplace=True)

    # 绘制堆叠条形图
    ax = stacked_data.plot(kind='bar', stacked=True, figsize=figsize, colormap='tab20')

    # 设置图表标题和标签
    plt.title(title, fontsize=16)
    plt.xlabel('Road Type', fontsize=12)
    plt.ylabel('Proportion of Total Vehicles (%)', fontsize=12)

    # 设置y轴为百分比格式
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.1f}%'))

    # 设置x轴标签旋转角度
    plt.xticks(rotation=45)

    # 添加图例
    plt.legend(title='Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')

    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()
    
