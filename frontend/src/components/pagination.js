import React, { Component, Fragment } from 'react';

const range = (from, to, step = 1) => {
    let i = from;
    const range = [];

    while (i <= to) {
        range.push(i);
        i += step;
    }

    return range;
}

const LEFT_PAGE = 'LEFT';
const RIGHT_PAGE = 'RIGHT';

class Pagination extends Component {
    goToPage = (page) => {
        this.props.onPageChanged(page);
    }

    moveRight = () => {
        this.goToPage(this.props.currentPage + 1);
    }

    moveLeft = () => {
        this.goToPage(this.props.currentPage - 1);
    }

    getPageNumbers = () => {
        const totalPages = this.props.totalPages;
        const pageNeighbors = this.props.pageNeighbors;
        const currentPage = this.props.currentPage;

        let viewablePages = [];

        const leftmost_neighbor = Math.max(1, this.props.currentPage - pageNeighbors);
        const rightmost_neighbor = Math.min(totalPages, this.props.currentPage + pageNeighbors);

        if (leftmost_neighbor > 1) {
            viewablePages.push(1);
        }

        if (currentPage > 1) {
            viewablePages.push(LEFT_PAGE);
        }

        viewablePages = viewablePages.concat(range(leftmost_neighbor, currentPage - 1));
        viewablePages.push(currentPage);
        viewablePages = viewablePages.concat(range(currentPage + 1, rightmost_neighbor));

        if (currentPage < totalPages) {
            viewablePages.push(RIGHT_PAGE);
        }

        if (rightmost_neighbor < totalPages) {
            viewablePages.push(totalPages);
        }

        return viewablePages;
    }

    render() {
        if (!this.props.totalPages || this.props.totalPages === 1) return null;

        const viewablePages = this.getPageNumbers();

        return (
            <Fragment>
                <nav aria-label="Pagination">
                    <ul className="pagination">
                        { viewablePages.map((page, index) => {
                            if (page === LEFT_PAGE) return (
                                <li key={index} className="page-item">
                                <a className="page-link" href="#" aria-label="Previous" onClick={this.moveLeft}>
                                    <span aria-hidden="true">&laquo;</span>
                                    <span className="sr-only">Previous</span>
                                </a>
                                </li>
                            )

                            if (page === RIGHT_PAGE) return (
                                <li key={index} className="page-item">
                                <a className="page-link" href="#" aria-label="Next" onClick={this.moveRight}>
                                    <span aria-hidden="true">&raquo;</span>
                                    <span className="sr-only">Next</span>
                                </a>
                                </li>
                            )

                            return (
                            <li key={index} className={`page-item${ this.props.currentPage === page ? ' active' : ''}`}>
                                <a className="page-link" href="#" onClick={ () => this.goToPage(page) }>{ page }</a>
                            </li>
                            );
                        })}
                    </ul>
                </nav>
            </Fragment>
        );
    }
}

export default Pagination;