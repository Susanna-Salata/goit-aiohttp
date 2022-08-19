import aiohttp.web
import aiohttp_jinja2
from src.db import Rate, Source, Currency


@aiohttp_jinja2.template('index.html')
def index(request):
    rates = request.app['db_session'].query(Rate).all()
    return {"rates": rates}


@aiohttp_jinja2.template('detail.html')
def detail(request):
    currency_id = request.match_info.get('currency_id')
    rates = request.app['db_session'].query(Rate, Source, Currency).filter(Rate.currency_id == currency_id,
                                                                           Currency.id == currency_id,
                                                                           Source.id == Rate.source_id).all()
    if not rates:
        return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
    return {"rates": rates}


@aiohttp_jinja2.template('source.html')
def source(request):
    sources = request.app['db_session'].query(Source).all()
    return {"sources": sources}


@aiohttp_jinja2.template('currency.html')
def currency(request):
    currencies = request.app['db_session'].query(Currency).all()
    return {"currencies": currencies}


async def create_rate(request):
    data = await request.post()
    rate_line = Rate(rate=data["rate"], currency_id=data["currency_id"], source_id=data["source_id"])
    request.app['db_session'].add(rate_line)
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def create_source(request):
    data = await request.post()
    source = Source(url=data["url"])
    request.app['db_session'].add(source)
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def create_currency(request):
    data = await request.post()
    currency_id = data["id"]
    currency_code = data["code"]
    currency_sign = data["sign"]
    currency_line = Currency(id=currency_id, code=currency_code, sign=currency_sign)
    request.app['db_session'].add(currency_line)
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def delete_rate(request):
    rate_id = request.match_info.get('rate_id')
    request.app['db_session'].query(Rate).filter(Rate.id == rate_id).delete()
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def done_rate(request):
    rate_id = request.match_info.get('rate_id')
    request.app['db_session'].query(Rate).filter(Rate.id == rate_id).first().done = True
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
