from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.products.schemas import ProductCreate, ProductRead, ProductUpdate
from app.modules.products.service import (
    DuplicateSKUError,
    ProductNotFoundError,
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def read_products(db: Session = Depends(get_db)) -> list[ProductRead]:  # noqa: B008
    return list_products(db)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def add_product(
    product_data: ProductCreate, db: Session = Depends(get_db)  # noqa: B008
) -> ProductRead:
    try:
        return create_product(db, product_data)
    except DuplicateSKUError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        ) from exc


@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, db: Session = Depends(get_db)) -> ProductRead:  # noqa: B008
    try:
        return get_product(db, product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc


@router.patch("/{product_id}", response_model=ProductRead)
def edit_product(
    product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)  # noqa: B008
) -> ProductRead:
    try:
        return update_product(db, product_id, product_data)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc
    except DuplicateSKUError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        ) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: int, db: Session = Depends(get_db)) -> None:  # noqa: B008
    try:
        delete_product(db, product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc
