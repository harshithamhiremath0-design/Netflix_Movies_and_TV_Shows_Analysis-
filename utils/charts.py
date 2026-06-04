import plotly.express as px

def movies_vs_tv(df):

    fig = px.pie(
        df,
        names='type',
        title='Movies vs TV Shows'
    )

    return fig


def release_year_chart(df):

    yearly = df.groupby('release_year').size().reset_index(name='count')

    fig = px.line(
        yearly,
        x='release_year',
        y='count',
        markers=True,
        title='Content Released by Year'
    )

    return fig


def top_countries(df):

    country_df = (
        df['country']
        .str.split(',')
        .explode()
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_df.columns = ['Country', 'Count']

    fig = px.bar(
        country_df,
        x='Country',
        y='Count',
        title='Top Countries'
    )

    return fig


def rating_chart(df):

    rating = df['rating'].value_counts().reset_index()

    rating.columns = ['Rating', 'Count']

    fig = px.bar(
        rating,
        x='Rating',
        y='Count',
        title='Content Rating Distribution'
    )

    return fig
