CREATE TYPE orderside AS ENUM ('buy', 'sell');
CREATE TYPE orderstatus AS ENUM ('open', 'maker', 'taker', 'canceled');
CREATE TYPE environment AS ENUM ('PAPER', 'PRODUCTION');
CREATE TYPE granularity AS ENUM ('1M', '5M', '15M', '30M', '1H', '6H', '1D');
CREATE TABLE IF NOT EXISTS candle (
    product text PRIMARY KEY,
    tstamp timestamp NOT NULL,
    timescale granularity NOT NULL,
    open double NOT NULL,
    high double NOT NULL,
    low double NOT NULL,
    close double NOT NULL,
    volume double NOT NULL,
);
CREATE INDEX ON candle(product);
CREATE INDEX ON candle(tstamp);
CREATE INDEX ON candle(timescale);
CREATE TABLE IF NOT EXISTS order (
    order_id text PRIMARY KEY,
    product text NOT NULL,
    tstamp timestamp NOT NULL,
    status orderstatus NOT NULL,
    side orderside NOT NULL,
    amount double NOT NULL,
    price double NOT NULL,
);
CREATE INDEX ON order(product);
CREATE INDEX ON order(tstamp);
CREATE INDEX ON order(status);
CREATE INDEX ON order(side);
CREATE TABLE IF NOT EXISTS indicator (
    product TEXT NOT NULL,
    tstamp datetime NOT NULL,
    timescale granularity NOT NULL,
    name TEXT NOT NULL,
    data TEXT NOT NULL,
);
CREATE INDEX ON indicator(product);
CREATE INDEX ON indicator(tstamp);
CREATE INDEX ON indicator(timescale);
CREATE INDEX ON indicator(name);
CREATE TABLE IF NOT EXISTS account (
    account_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    currency TEXT NOT NULL,
    balance double NOT NULL,
    available double NOT NULL ,
    enabled boolean NOT NULL,
);
