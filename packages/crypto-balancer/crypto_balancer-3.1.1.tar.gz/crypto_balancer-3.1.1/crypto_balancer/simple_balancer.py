from crypto_balancer.order import Order


class Attempt():
    def __init__(self, portfolio, orders=None, total_fee=0.0, depth=0,
                 pairs_processed=None):
        self.portfolio = portfolio
        self.orders = orders or []
        self.total_fee = total_fee
        self.depth = depth
        self.pairs_processed = pairs_processed or set()


class SimpleBalancer():

    def permute_differences(self, differences_quote):
        differences = differences_quote.items()
        positives = [x for x in differences if x[1] > 0.01]
        negatives = [x for x in differences if x[1] < -0.01]
        res = []
        for p in sorted(positives, key=lambda x: x[1], reverse=True):
            for n in sorted(negatives, key=lambda x: x[1]):
                if p[0] != n[0]:
                    res.append((p, n))
        return res

    def balance(self, initial_portfolio, exchange, max_orders=5):
        rates = exchange.rates
        quote_currency = initial_portfolio.quote_currency

        # Add in the identify rate just so we don't have to special
        # case it later
        rates["{}/{}".format(quote_currency, quote_currency)] = 1.0

        todo = [Attempt(initial_portfolio)]
        attempts = []

        while todo:
            attempt = todo.pop()
            diffs = self.permute_differences(
                attempt.portfolio.differences_quote)

            if not diffs or attempt.depth >= max_orders:
                continue

            for pos, neg in diffs:
                p_cur, p_amount = pos
                n_cur, n_amount = neg

                trade_direction = None

                # try and see if we have the pair we need
                # and if so, buy it
                pair = "{}/{}".format(p_cur, n_cur)
                if pair in rates:
                    trade_direction = "BUY"
                    trade_pair = pair

                # if previous failed then reverse paid and try
                # sell instead
                pair = "{}/{}".format(n_cur, p_cur)
                if pair in rates:
                    trade_direction = "SELL"
                    trade_pair = pair

                if not trade_direction:
                    continue

                if trade_pair in attempt.pairs_processed:
                    continue

                # Calculate the min order for this pair
                min_trade_amount_quote = \
                    exchange.limits[trade_pair]['cost']['min']

                # Work out the pair to get to the quote currency
                to_sell_pair_quote = "{}/{}".format(n_cur, quote_currency)
                to_buy_pair_quote = "{}/{}".format(p_cur, quote_currency)

                for trade_amount_quote in (p_amount,
                                           -n_amount,
                                           min_trade_amount_quote,
                                           min_trade_amount_quote * 1.5):

                    # Work out how much of the currency to buy/sell
                    to_sell_amount_cur = \
                        trade_amount_quote / rates[to_sell_pair_quote]
                    to_buy_amount_cur = \
                        trade_amount_quote / rates[to_buy_pair_quote]

                    if trade_direction == "BUY":
                        trade_amount = to_buy_amount_cur

                    if trade_direction == "SELL":
                        trade_amount = to_sell_amount_cur

                    # We got a direction, so we know we can either
                    # buy or sell this pair
                    trade_rate = rates[trade_pair]
                    order = Order(trade_pair, trade_direction,
                                  trade_amount, trade_rate)

                    order = exchange.preprocess_order(order)
                    if not order:
                        continue

                    # Adjust the amounts of each currency we hold
                    new_portfolio = attempt.portfolio.copy()

                    new_portfolio.balances[p_cur] \
                        += to_buy_amount_cur
                    new_portfolio.balances[n_cur] \
                        -= to_sell_amount_cur

                    if new_portfolio.balances[n_cur] < 0:
                        # gone negative so not valid result
                        break

                    fee = trade_amount_quote * exchange.fee
                    new_attempt = Attempt(new_portfolio,
                                          sorted(attempt.orders + [order]),
                                          attempt.total_fee + fee,
                                          attempt.depth + 1,
                                          attempt.pairs_processed | set(
                                              [trade_pair]
                                          ))
                    todo.append(new_attempt)

                    if new_attempt.portfolio.balance_rms_error < \
                       initial_portfolio.balance_rms_error:
                        attempts.append(new_attempt)

        if not attempts:
            return {'orders': [],
                    'total_fee': 0.0,
                    'initial_portfolio': initial_portfolio,
                    'proposed_portfolio': None}

        sort_key = lambda x: (x.portfolio.balance_rms_error,
                              x.total_fee,
                              len(x.orders),
                              x.orders)
        decorated_attempts = [(sort_key(x), x) for x in attempts]
        decorated_attempts.sort(key=lambda x: x[0])
        best_attempt = decorated_attempts[0][1]

        return {'orders': sorted(best_attempt.orders),
                'total_fee': best_attempt.total_fee,
                'initial_portfolio': initial_portfolio,
                'proposed_portfolio': best_attempt.portfolio}
