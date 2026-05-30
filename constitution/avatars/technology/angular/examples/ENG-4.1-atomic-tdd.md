---
law_id: ENG-4.1
avatar: angular
---

# ENG-4.1: Atomic TDD Examples for Angular

## COMPLIANT: Test-First Development with Jasmine and TestBed

```typescript
// user-profile.component.spec.ts
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { UserProfileComponent } from './user-profile.component';
import { UserService } from '../services/user.service';
import { of, throwError } from 'rxjs';

describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;
  let userServiceSpy: jasmine.SpyObj<UserService>;

  const mockUser = {
    id: '1',
    name: 'Jane Doe',
    email: 'jane@example.com'
  };

  beforeEach(async () => {
    userServiceSpy = jasmine.createSpyObj('UserService', ['getUser']);

    await TestBed.configureTestingModule({
      imports: [UserProfileComponent],
      providers: [
        { provide: UserService, useValue: userServiceSpy }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
  });

  // Step 1: Write tests FIRST (Red phase)
  it('should display user name after loading', fakeAsync(() => {
    userServiceSpy.getUser.and.returnValue(of(mockUser));
    component.userId = '1';

    fixture.detectChanges();
    tick();
    fixture.detectChanges();

    const heading = fixture.debugElement.query(By.css('[data-testid="user-name"]'));
    expect(heading.nativeElement.textContent).toContain('Jane Doe');
  }));

  it('should show loading state initially', () => {
    userServiceSpy.getUser.and.returnValue(of(mockUser));
    component.userId = '1';

    fixture.detectChanges();

    const loading = fixture.debugElement.query(By.css('[role="status"]'));
    expect(loading).toBeTruthy();
    expect(loading.nativeElement.textContent).toContain('Loading');
  });

  it('should handle error state gracefully', fakeAsync(() => {
    userServiceSpy.getUser.and.returnValue(throwError(() => new Error('Network error')));
    component.userId = '1';

    fixture.detectChanges();
    tick();
    fixture.detectChanges();

    const alert = fixture.debugElement.query(By.css('[role="alert"]'));
    expect(alert).toBeTruthy();
    expect(alert.nativeElement.textContent).toContain('Failed to load user');
  }));

  it('should call user service with correct ID', () => {
    userServiceSpy.getUser.and.returnValue(of(mockUser));
    component.userId = '42';

    fixture.detectChanges();

    expect(userServiceSpy.getUser).toHaveBeenCalledWith('42');
  });
});
```

```typescript
// user-profile.component.ts - Step 2: Minimal implementation (Green phase)
import { Component, Input, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../services/user.service';

interface User {
  id: string;
  name: string;
  email: string;
}

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div *ngIf="loading" role="status" aria-label="Loading">Loading...</div>
    <div *ngIf="error" role="alert">{{ error }}</div>
    <article *ngIf="user && !loading && !error">
      <h1 data-testid="user-name">{{ user.name }}</h1>
      <p>{{ user.email }}</p>
    </article>
  `
})
export class UserProfileComponent implements OnInit {
  private userService = inject(UserService);

  @Input({ required: true }) userId!: string;

  user: User | null = null;
  loading = true;
  error: string | null = null;

  ngOnInit(): void {
    this.userService.getUser(this.userId).subscribe({
      next: (user) => {
        this.user = user;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load user';
        this.loading = false;
      }
    });
  }
}
```

**Why compliant:** Tests are written before implementation following Red-Green-Refactor. Each test is atomic, testing one specific behavior. Uses TestBed for proper Angular dependency injection. Spy objects isolate the component from external services.

---

## COMPLIANT: Testing Component Interactions Atomically

```typescript
// counter.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should start at zero by default', () => {
    const display = fixture.debugElement.query(By.css('[data-testid="counter-value"]'));
    expect(display.nativeElement.textContent).toBe('0');
  });

  it('should start at provided initial value', () => {
    component.initialValue = 5;
    component.ngOnInit();
    fixture.detectChanges();

    const display = fixture.debugElement.query(By.css('[data-testid="counter-value"]'));
    expect(display.nativeElement.textContent).toBe('5');
  });

  it('should increment when plus button is clicked', () => {
    const incrementBtn = fixture.debugElement.query(By.css('[aria-label="Increment"]'));
    incrementBtn.triggerEventHandler('click', null);
    fixture.detectChanges();

    const display = fixture.debugElement.query(By.css('[data-testid="counter-value"]'));
    expect(display.nativeElement.textContent).toBe('1');
  });

  it('should decrement when minus button is clicked', () => {
    component.initialValue = 5;
    component.ngOnInit();
    fixture.detectChanges();

    const decrementBtn = fixture.debugElement.query(By.css('[aria-label="Decrement"]'));
    decrementBtn.triggerEventHandler('click', null);
    fixture.detectChanges();

    const display = fixture.debugElement.query(By.css('[data-testid="counter-value"]'));
    expect(display.nativeElement.textContent).toBe('4');
  });

  it('should not go below minimum value', () => {
    component.min = 0;
    component.initialValue = 0;
    component.ngOnInit();
    fixture.detectChanges();

    const decrementBtn = fixture.debugElement.query(By.css('[aria-label="Decrement"]'));
    decrementBtn.triggerEventHandler('click', null);
    fixture.detectChanges();

    const display = fixture.debugElement.query(By.css('[data-testid="counter-value"]'));
    expect(display.nativeElement.textContent).toBe('0');
  });

  it('should emit valueChange event when value changes', () => {
    spyOn(component.valueChange, 'emit');

    const incrementBtn = fixture.debugElement.query(By.css('[aria-label="Increment"]'));
    incrementBtn.triggerEventHandler('click', null);

    expect(component.valueChange.emit).toHaveBeenCalledWith(1);
  });
});
```

**Why compliant:** Each test focuses on a single atomic behavior. Tests are independent and can run in any order. User interactions are tested through template event triggering. Output events are verified using spies.

---

## COMPLIANT: Testing Services with HttpClientTestingModule

```typescript
// user.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { UserService } from './user.service';

describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });

    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Verify no outstanding requests
  });

  it('should fetch user by ID', () => {
    const mockUser = { id: '1', name: 'Jane Doe', email: 'jane@example.com' };

    service.getUser('1').subscribe(user => {
      expect(user).toEqual(mockUser);
    });

    const req = httpMock.expectOne('/api/users/1');
    expect(req.request.method).toBe('GET');
    req.flush(mockUser);
  });

  it('should handle 404 error', () => {
    service.getUser('999').subscribe({
      next: () => fail('should have failed'),
      error: (error) => {
        expect(error.status).toBe(404);
      }
    });

    const req = httpMock.expectOne('/api/users/999');
    req.flush('User not found', { status: 404, statusText: 'Not Found' });
  });

  it('should create new user', () => {
    const newUser = { name: 'John Doe', email: 'john@example.com' };
    const createdUser = { id: '2', ...newUser };

    service.createUser(newUser).subscribe(user => {
      expect(user).toEqual(createdUser);
    });

    const req = httpMock.expectOne('/api/users');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(newUser);
    req.flush(createdUser);
  });
});
```

**Why compliant:** Uses HttpClientTestingModule for isolated HTTP testing. Each test verifies one specific API behavior. afterEach ensures no unexpected HTTP calls. Tests cover success and error scenarios atomically.

---

## VIOLATION: Testing Implementation Details

```typescript
// BAD: user-profile.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UserProfileComponent } from './user-profile.component';

describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserProfileComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
  });

  it('should set loading to true initially', () => {
    // Testing private implementation details
    expect(component['loading']).toBe(true);
  });

  it('should have correct lifecycle hooks', () => {
    // Testing that methods exist, not behavior
    expect(component.ngOnInit).toBeDefined();
    expect(component.ngOnDestroy).toBeDefined();
  });

  it('should have subscription property', () => {
    // Testing internal state
    expect(component['userSubscription']).toBeUndefined();
    fixture.detectChanges();
    expect(component['userSubscription']).toBeDefined();
  });

  it('should call detectChanges internally', () => {
    // Spying on framework internals
    const cdSpy = spyOn(component['cd'], 'detectChanges');
    fixture.detectChanges();
    component['fetchUser']();
    expect(cdSpy).toHaveBeenCalled();
  });
});
```

**Why violates ENG-4.1:** Tests access private properties and methods directly. Tests verify implementation details like subscriptions and change detection calls. These tests will break during refactoring even if behavior remains correct. Tests should verify what users see, not internal mechanics.

---

## VIOLATION: Non-Atomic Tests with Multiple Behaviors

```typescript
// BAD: login-form.component.spec.ts
import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';
import { LoginFormComponent } from './login-form.component';

describe('LoginFormComponent', () => {
  let component: LoginFormComponent;
  let fixture: ComponentFixture<LoginFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginFormComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should handle complete login flow', fakeAsync(() => {
    // BEHAVIOR 1: Form should render correctly
    expect(fixture.nativeElement.querySelector('input[type="email"]')).toBeTruthy();
    expect(fixture.nativeElement.querySelector('input[type="password"]')).toBeTruthy();
    expect(fixture.nativeElement.querySelector('button[type="submit"]')).toBeTruthy();

    // BEHAVIOR 2: Empty form should show validation errors
    const submitBtn = fixture.nativeElement.querySelector('button[type="submit"]');
    submitBtn.click();
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Email is required');
    expect(fixture.nativeElement.textContent).toContain('Password is required');

    // BEHAVIOR 3: Invalid email should show error
    const emailInput = fixture.nativeElement.querySelector('input[type="email"]');
    emailInput.value = 'invalid';
    emailInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Invalid email');

    // BEHAVIOR 4: Valid input should clear errors
    emailInput.value = 'test@example.com';
    emailInput.dispatchEvent(new Event('input'));
    const passwordInput = fixture.nativeElement.querySelector('input[type="password"]');
    passwordInput.value = 'password123';
    passwordInput.dispatchEvent(new Event('input'));
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).not.toContain('Email is required');

    // BEHAVIOR 5: Form submission
    submitBtn.click();
    tick();
    fixture.detectChanges();
    expect(component.submitted).toBe(true);

    // BEHAVIOR 6: Loading state during submission
    expect(fixture.nativeElement.querySelector('.loading-spinner')).toBeTruthy();
  }));
});
```

**Why violates ENG-4.1:** Test combines 6 different behaviors into one test. When it fails, unclear which behavior is broken. Tests should follow "one behavior per test" principle. Each scenario (validation, submission, loading) should be tested separately.

---

## VIOLATION: Tests Without Proper Isolation

```typescript
// BAD: shared-state.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SharedStateComponent } from './shared-state.component';
import { StateService } from '../services/state.service';

// Using real service instead of mock
const stateService = new StateService();

describe('SharedStateComponent', () => {
  let component: SharedStateComponent;
  let fixture: ComponentFixture<SharedStateComponent>;

  beforeEach(async () => {
    // Not resetting state between tests!
    await TestBed.configureTestingModule({
      imports: [SharedStateComponent],
      providers: [
        { provide: StateService, useValue: stateService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(SharedStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  // These tests depend on each other and run order
  it('should have empty state initially', () => {
    expect(stateService.getItems().length).toBe(0);
  });

  it('should add item to state', () => {
    stateService.addItem({ id: '1', name: 'Test' });
    expect(stateService.getItems().length).toBe(1);
  });

  it('should have one item', () => {
    // FAILS if run alone! Depends on previous test
    expect(stateService.getItems().length).toBe(1);
  });

  it('should add another item', () => {
    stateService.addItem({ id: '2', name: 'Test 2' });
    // Depends on accumulated state from previous tests
    expect(stateService.getItems().length).toBe(2);
  });
});
```

**Why violates ENG-4.1:** Tests share state through real service instance. Tests depend on execution order. Running tests in isolation will fail. Each test should be independent with fresh state. Should use jasmine spies or fresh mock instances.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
ng test --include="**/user-profile.component.spec.ts" --watch=false

# GREEN: Write code, run test again
ng test --include="**/user-profile.component.spec.ts" --watch=false

# REFACTOR: Run all unit tests
ng test --watch=false

# VERIFY: Check coverage and constitutional compliance
ng test --watch=false --code-coverage
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add user profile component"
```
